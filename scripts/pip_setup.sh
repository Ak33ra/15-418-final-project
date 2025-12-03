#!/usr/bin/env bash
# Intended to set up dependencies on rented GPU with pip
# Usage:
#   chmod +x pip_setup.sh
#   ./pip_setup.sh
set -euo pipefail

# ----------------------------
# CONFIG
# ----------------------------
VENV_DIR=".venv"

# ----------------------------
# CREATE VENV
# ----------------------------
echo "[info] Creating virtual environment in $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

# ----------------------------
# ACTIVATE
# ----------------------------
echo "[info] Activating venv..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------
if [ -f requirements.txt ]; then
    echo "[info] Installing requirements.txt..."
    pip install -r requirements.txt
else
    echo "[warn] No requirements.txt found, skipping."
fi

# ----------------------------
# INSTALL PROJECT IN EDITABLE MODE
# ----------------------------
echo "[info] Installing project in editable mode (pip install -e .)..."
pip install -e .

echo "[success] Virtual environment is ready!"
echo "[success] To activate later: source $VENV_DIR/bin/activate"

