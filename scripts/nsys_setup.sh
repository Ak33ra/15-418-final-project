#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/setup_nsys.sh /path/to/nsight-systems.deb
#   scripts/setup_nsys.sh https://.../nsight-systems-xxx.deb
#
# Optional:
#   NSYS_PREFIX=/some/path scripts/setup_nsys.sh nsight-systems.deb
#
# After running:
#   export PATH="$NSYS_PREFIX/bin:$PATH"

PKG_SRC="${1:-}"

if [[ -z "$PKG_SRC" ]]; then
    echo "Usage: $0 <nsight-systems .deb/.rpm path or URL>"
    exit 1
fi

# Where to install (default: repo-local)
NSYS_PREFIX="${NSYS_PREFIX:-$PWD/vendor/nsight-systems}"

echo "[nsys setup] Install prefix: $NSYS_PREFIX"
mkdir -p "$NSYS_PREFIX"

# -------------------------------
# Fetch package (if URL)
# -------------------------------
TMP_PKG=""
if [[ "$PKG_SRC" =~ ^https?:// ]]; then
    echo "[nsys setup] Downloading package from URL..."
    TMP_PKG="$(mktemp)"
    curl -L "$PKG_SRC" -o "$TMP_PKG"
    PKG="$TMP_PKG"
else
    PKG="$PKG_SRC"
fi

if [[ ! -f "$PKG" ]]; then
    echo "[nsys setup] ERROR: package not found: $PKG"
    exit 1
fi

# -------------------------------
# Extract package (no sudo)
# -------------------------------
case "$PKG" in
    *.deb)
        echo "[nsys setup] Detected .deb package, using dpkg-deb..."
        dpkg-deb -x "$PKG" "$NSYS_PREFIX"
        ;;
    *.rpm)
        echo "[nsys setup] Detected .rpm package, using rpm2cpio + cpio..."
        if ! command -v rpm2cpio >/dev/null 2>&1; then
            echo "[nsys setup] ERROR: rpm2cpio not found. Install it or use a .deb."
            exit 1
        fi
        ( cd "$NSYS_PREFIX" && rpm2cpio "$PKG" | cpio -idmv )
        ;;
    *)
        echo "[nsys setup] ERROR: unknown package type (expected .deb or .rpm): $PKG"
        exit 1
        ;;
esac

# Clean up temp download if used
if [[ -n "${TMP_PKG}" && -f "${TMP_PKG}" ]]; then
    rm -f "$TMP_PKG"
fi

# -------------------------------
# Locate CLI target dir
# -------------------------------
TARGET_DIR="$(find "$NSYS_PREFIX" -maxdepth 8 -type d -name 'target-linux-*' | head -n 1 || true)"

if [[ -z "$TARGET_DIR" ]]; then
    echo "[nsys setup] ERROR: could not find Nsight Systems target-linux-* directory in $NSYS_PREFIX"
    exit 1
fi

NSYS_BIN="${TARGET_DIR}/nsys"

if [[ ! -x "$NSYS_BIN" ]]; then
    echo "[nsys setup] ERROR: nsys binary not found or not executable at $NSYS_BIN"
    exit 1
fi

# -------------------------------
# Create a clean bin/ wrapper
# -------------------------------
BIN_DIR="${NSYS_PREFIX}/bin"
mkdir -p "$BIN_DIR"
ln -sf "$NSYS_BIN" "${BIN_DIR}/nsys"

echo
echo "[nsys setup] Success!"
echo "[nsys setup] nsys binary: $NSYS_BIN"
echo
echo "Add this to your shell:"
echo
echo "    export PATH=\"$BIN_DIR:\$PATH\""
echo
echo "Then verify:"
echo
echo "    nsys --version"
echo
