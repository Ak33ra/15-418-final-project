#!/usr/bin/env python
"""
CLI wrapper around multitenant.runners.single_model_runner.run_single_model

Usage:

Run from YAML config:
  python scripts/bench_single_model.py \
      --config experiments/configs/distilgpt2_solo

Run from CLI args:
  python scripts/bench_single_model.py \
      --model distilgpt2 \
      --batch-size 8 \
      --seq-len 128 \
      --num-iters 100 \
      --out_dir experiments/logs \
      --tag solo_distilgpt2
"""

from pathlib import Path
import argparse
import sys
import yaml
import torch

from multitenant.single_model_runner import (
    SingleModelConfig,
    run_single_model,
)

def parse_args() -> argparse.Namespace:
    """
    Parses script CLI arguments
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=None,
                    help="YAML config file for a single model experiment")
    ap.add_argument("--model", type=str, default="distilgpt2",
                    help="HF model name or local path")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--seq-len", type=int, default=128)
    ap.add_argument("--num-warmup", type=int, default=10)
    ap.add_argument("--num-iters", type=int, default=100)
    ap.add_argument("--device", type=str, default="cuda",
                    help="'cuda' or 'cpu'")
    ap.add_argument("--out-dir", type=str, default="experiments/logs",
                    help="Directory to write latency logs")
    ap.add_argument("--tag", type=str, default="solo",
                    help="Tag to include in output filenames")
    ap.add_argument("--no-save",type=bool, default=False,
                     help="Whether or not to write metrics to out_dir")
    ap.add_argument("--verbose",type=bool, default=True)
    return ap.parse_args()


def main() -> None:
    """
    Loads and runs experiment and model config from YAML or command-line arguments.

    Prints summary of performance metrics to stdout and writes results to out_dir.
    """
    args = parse_args()
    if args.config:
        cfg_path = Path(args.config)
        with cfg_path.open(mode="r", encoding="utf-8") as f:
            cfg_yaml = yaml.safe_load(f)
        single_model_dict = cfg_yaml.get("single_model", {})
        cfg = SingleModelConfig(**single_model_dict)
        print(f"[bench] Loaded config from {cfg_path}")
    else:
        cfg = SingleModelConfig(
            model_name=args.model,
            batch_size=args.batch_size,
            seq_len=args.seq_len,
            num_warmup=args.num_warmup,
            num_iters=args.num_iters,
            device=args.device,
            out_dir=args.out_dir,
            tag=args.tag,
        )
        print("[bench] Using CLI arguments for config")

    print(f"out dir: {cfg.out_dir}")

    barrier = None
    result = run_single_model(cfg, args.no_save, barrier, args.verbose)

    if args.verbose:
        print("\n=== Summary (from script) ===")
        print(f"Model:      {cfg.model_name}")
        print(f"Tag:        {cfg.tag}")
        print(f"Avg (ms):   {result.avg_ms:.3f}")
        print(f"p95 (ms):   {result.p95_ms:.3f}")
        print(f"Throughput: {result.throughput_tokens_per_s:.2f} tokens/s")

    # Sync CUDA to ensure process terminates
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        torch.cuda.empty_cache()

    sys.exit(0)

if __name__ == "__main__":
    main()
