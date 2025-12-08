#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="configs/multitenants"

echo "Running all multitenant configs in: $CONFIG_DIR"
echo

for cfg in "$CONFIG_DIR"/*.yaml "$CONFIG_DIR"/*.yml; do
    # Skip if no files match
    [ -e "$cfg" ] || continue

    cfg_name="$(basename "$cfg")"

    echo "==> Running config: $cfg_name"
    ./scripts/bench_multitenants.py --config "$CONFIG_DIR"/"$cfg_name" --verbose False
    echo
done

echo "All configs completed."
