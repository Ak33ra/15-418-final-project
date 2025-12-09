#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="configs/multitenant"

echo "Running NSYS profiling for all multitenant configs..."
echo

for cfg in "$CONFIG_DIR"/*.yaml "$CONFIG_DIR"/*.yml; do
    [ -e "$cfg" ] || continue

    cfg_name="$(basename "$cfg")"

    # ---- Extract experiment_name from YAML ----
    # Assumes a line like: experiment_name: my_exp
    experiment_name=$(grep -E '^experiment_name:' "$cfg" \
        | awk '{print $2}' \
        | tr -d '"')
    if [ -z "$experiment_name" ]; then
        echo "[ERROR] No experiment_name found in $cfg"
        exit 1
    fi

    OUT_DIR="out/nsys/$experiment_name"
    mkdir -p "$OUT_DIR"

    echo "==> Config: $cfg_name"
    echo "    experiment_name = $experiment_name"
    echo "    Output directory = $OUT_DIR"
    echo

    # ---- Run NSYS ----
    nsys profile \
        -o "$OUT_DIR"/"$experiment_name" \
        --trace=cuda,nvtx,osrt \
        --gpu-metrics-device=all \
        --sample=gpu \
        python scripts/bench_multitenants.py \
            --config "$CONFIG_DIR"/"$cfg_name" \
            --no-save true \
            --verbose false

    echo
done

echo "All NSYS profiles completed."
