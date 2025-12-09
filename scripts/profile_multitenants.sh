#!/usr/bin/env bash
set -euo pipefail

# Usage:
# ./scripts/profile_multitenants.sh --config path/to/multitenant/config --out out/file/prefix
#
# Example:
# ./scripts/profile_multitenants.sh \
#   --config configs/multitenant/nomps_distilgpt2.yaml
#   --out out/nsys/distilgpt2

# Default values (can be overridden by CLI)
CONFIG=""
OUT_PREFIX=""

# -----------------------------
# Parse arguments
# -----------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --out)
            OUT_PREFIX="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --config <config.yaml> --out <output_prefix> [additional args]"
            exit 1
            ;;
    esac
done

if [[ -z "$CONFIG" ]]; then
    echo "ERROR: --config is required"
    exit 1
fi

if [[ -z "$OUT_PREFIX" ]]; then
    echo "ERROR: --out is required"
    exit 1
fi

# Make sure output dir exists
OUT_DIR="$(dirname "$OUT_PREFIX")"
mkdir -p "$OUT_DIR"

echo "[profile] Config: $CONFIG"
echo "[profile] Output prefix: $OUT_PREFIX"

# -----------------------------
# Run Nsight Systems
# -----------------------------
nsys profile \
    -o "$OUT_PREFIX" \
    --trace=cuda,nvtx,osrt \
    --gpu-metrics-device=all \
    --sample=gpu \
    python scripts/bench_multitenants.py \
        --config "$CONFIG" \
        --no-save true \
        --verbose true
