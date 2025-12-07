#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------
# Usage: nsys_extract_stats.sh <directory>
# Automatically finds *.nsys-rep in that directory,
# runs all four stats reports, and writes outputs
# back into that same directory.
# ---------------------------------------------------------

# Example Usage:
# ./scripts/nsys_extract_stats.sh out/nsys/mps_pair_distilgpt2

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <directory-containing-nsys-rep>"
    exit 1
fi

TARGET_DIR="$1"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "ERROR: Directory not found: $TARGET_DIR"
    exit 1
fi

# ---------------------------------------------------------
# Locate .nsys-rep file (must be exactly one)
# ---------------------------------------------------------
shopt -s nullglob
REP_FILES=( "$TARGET_DIR"/*.nsys-rep )

if [[ ${#REP_FILES[@]} -eq 0 ]]; then
    echo "ERROR: No .nsys-rep files found in: $TARGET_DIR"
    exit 1
elif [[ ${#REP_FILES[@]} -gt 1 ]]; then
    echo "ERROR: Multiple .nsys-rep files found. Please keep only one."
    printf '%s\n' "${REP_FILES[@]}"
    exit 1
fi

REP_FILE="${REP_FILES[0]}"

echo "[nsys stats] Found rep file: $REP_FILE"
echo "[nsys stats] Output directory: $TARGET_DIR"
echo

# ---------------------------------------------------------
# Reports → output filenames
# ---------------------------------------------------------
declare -A REPORTS=(
    ["gpu_kernel.json"]="cuda_gpu_kern_sum"
    ["cuda_api.json"]="cuda_api_sum"
    ["nvtx.json"]="nvtx_sum"
    ["osrt.json"]="osrt_sum"
)

# ---------------------------------------------------------
# Run reports
# ---------------------------------------------------------
for OUT_NAME in "${!REPORTS[@]}"; do
    REPORT="${REPORTS[$OUT_NAME]}"
    OUT_PATH="$TARGET_DIR/$OUT_NAME"

    echo "[nsys stats] Running report: $REPORT → $OUT_PATH"

    nsys stats \
        --report "$REPORT" \
        --format json \
        "$REP_FILE" \
        > "$OUT_PATH"
done

echo
echo "[nsys stats] All reports generated successfully:"
ls -1 "$TARGET_DIR" | sed 's/^/  - /'
