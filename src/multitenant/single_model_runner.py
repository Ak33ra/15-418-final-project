# src/multitenant/single_model_runner.py

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Tuple, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizerBase


@dataclass
class SingleModelConfig:
    model_name: str = "distilgpt2"
    batch_size: int = 8
    seq_len: int = 128
    num_warmup: int = 10
    num_iters: int = 100
    device: str = "cuda"
    out_dir: str = "experiments/logs"
    tag: str = "solo"


@dataclass
class SingleModelResult:
    avg_ms: float
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    throughput_tokens_per_s: float
    latencies_ms: List[float]
    config: SingleModelConfig


def load_model_and_tokenizer(
    model_name: str, device: torch.device
) -> Tuple[PreTrainedModel, PreTrainedTokenizerBase]:
    print(f"[load] Loading model '{model_name}' on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.to(device)
    model.eval()

    # For GPT-2 family: no pad token → set pad to eos for convenience
    if tokenizer.pad_token is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def make_synthetic_batch(
    tokenizer: PreTrainedTokenizerBase,
    batch_size: int,
    seq_len: int,
    device: torch.device,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Create a synthetic batch of token ids; no actual text needed."""
    vocab_size = tokenizer.vocab_size
    torch.manual_seed(0)
    input_ids = torch.randint(
        low=0,
        high=vocab_size,
        size=(batch_size, seq_len),
        dtype=torch.long,
        device=device,
    )
    attention_mask = torch.ones_like(input_ids, device=device)
    return input_ids, attention_mask


def _percentile(sorted_vals: List[float], q: float) -> float:
    """q in [0,1]; sorted_vals must be sorted ascending."""
    if not sorted_vals:
        return float("nan")
    idx = max(0, min(len(sorted_vals) - 1, int(q * len(sorted_vals)) - 1))
    return sorted_vals[idx]


def run_single_model(config: SingleModelConfig) -> SingleModelResult:
    device = torch.device(config.device)
    out_dir = Path(config.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model, tokenizer = load_model_and_tokenizer(config.model_name, device)
    input_ids, attention_mask = make_synthetic_batch(
        tokenizer, config.batch_size, config.seq_len, device
    )

    # Warmup
    print(f"[warmup] {config.num_warmup} iterations...")
    with torch.no_grad():
        for _ in range(config.num_warmup):
            _ = model(input_ids=input_ids, attention_mask=attention_mask)
    if device.type == "cuda":
        torch.cuda.synchronize()

    # Timed loop
    print(f"[run] {config.num_iters} timed iterations...")
    latencies_ms: List[float] = []

    # Time with CUDA events
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)

    with torch.no_grad():
        for i in range(config.num_iters):
            #t0 = time.perf_counter()
            start_event.record()
            _ = model(input_ids=input_ids, attention_mask=attention_mask)
            end_event.record()
            if device.type == "cuda":
                torch.cuda.synchronize()
            #t1 = time.perf_counter()
            #lat_ms = (t1 - t0) * 1e3
            lat_ms = start_event.elapsed_time(end_event)
            latencies_ms.append(lat_ms)

            if (i + 1) % max(1, config.num_iters // 10) == 0:
                print(f"  iter {i+1}/{config.num_iters}: {lat_ms:.3f} ms")

    latencies_ms.sort()
    avg = mean(latencies_ms)
    p50 = _percentile(latencies_ms, 0.50)
    p90 = _percentile(latencies_ms, 0.90)
    p95 = _percentile(latencies_ms, 0.95)
    p99 = _percentile(latencies_ms, 0.99)

    total_time_s = sum(latencies_ms) / 1e3
    tokens_processed = config.batch_size * config.seq_len * config.num_iters
    throughput = tokens_processed / total_time_s if total_time_s > 0 else 0.0

    result = SingleModelResult(
        avg_ms=avg,
        p50_ms=p50,
        p90_ms=p90,
        p95_ms=p95,
        p99_ms=p99,
        throughput_tokens_per_s=throughput,
        latencies_ms=latencies_ms,
        config=config,
    )

    # Write files
    base = (
        f"{config.tag}_"
        f"{config.model_name.replace('/', '_')}_"
        f"b{config.batch_size}_L{config.seq_len}"
    )
    lat_path = out_dir / f"{base}_latencies_ms.csv"
    meta_path = out_dir / f"{base}_summary.txt"

    with lat_path.open("w") as f:
        for x in latencies_ms:
            f.write(f"{x:.6f}\n")

    meta = {
        "avg_ms": result.avg_ms,
        "p50_ms": result.p50_ms,
        "p90_ms": result.p90_ms,
        "p95_ms": result.p95_ms,
        "p99_ms": result.p99_ms,
        "throughput_tokens_per_s": result.throughput_tokens_per_s,
        **{f"config_{k}": v for k, v in asdict(config).items()},
    }
    with meta_path.open("w") as f:
        for k, v in meta.items():
            f.write(f"{k}={v}\n")

    print(f"\n[write] Latencies → {lat_path}")
    print(f"[write] Summary   → {meta_path}")

    return result

