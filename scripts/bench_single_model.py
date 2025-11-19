#!/usr/bin/env python
"""
CLI wrapper around mps_multitenant.runners.single_model_runner.run_single_model

Usage:
  python scripts/bench_single_model.py \
      --model distilgpt2 \
      --batch-size 8 \
      --seq-len 128 \
      --num-iters 100 \
      --tag solo_distilgpt2
"""

import argparse

from mps_multitenant.runners.single_model_runner import (
    SingleModelConfig,
    run_single_model,
)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
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
    return ap.parse_args()


def main() -> None:
    args = parse_args()
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

    result = run_single_model(cfg)

    # Print a compact summary to stdout (the files already have details)
    print("\n=== Summary (from script) ===")
    print(f"Model:      {cfg.model_name}")
    print(f"Tag:        {cfg.tag}")
    print(f"Avg (ms):   {result.avg_ms:.3f}")
    print(f"p95 (ms):   {result.p95_ms:.3f}")
    print(f"Throughput: {result.throughput_tokens_per_s:.2f} tokens/s")


if __name__ == "__main__":
    main()

