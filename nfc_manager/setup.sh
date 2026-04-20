#!/usr/bin/env bash
# setup.sh — One-time (or repair) environment setup for NFC Tag Manager
# Run this first, or any time the venv is broken or dependencies change.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

echo "=== NFC Tag Manager — Setup ==="
echo "Project: $SCRIPT_DIR"
echo ""

# ── 1. Verify Python ─────────────────────────────────────────────────────────
PYTHON=$(command -v python3 || true)
if [[ -z "$PYTHON" ]]; then
    echo "ERROR: python3 not found. Install it with: sudo apt install python3"
    exit 1
fi

PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python:  $("$PYTHON" --version)  ($PYTHON)"
echo "Version: $PYTHON_VERSION"
echo ""

# ── 2. Check for python3-venv ─────────────────────────────────────────────────
if ! "$PYTHON" -c "import venv" 2>/dev/null; then
    echo "Installing python3-venv..."
    sudo apt-get install -y python3-venv
fi

# ── 3. Check for tkinter (required by customtkinter) ─────────────────────────
if ! "$PYTHON" -c "import tkinter" 2>/dev/null; then
    echo "Installing python3-tk..."
    sudo apt-get install -y python3-tk
fi

# ── 4. Remove stale venv if it was built for a different platform/version ─────
if [[ -d "$VENV_DIR" ]]; then
    VENV_PYTHON="$VENV_DIR/bin/python"
    VENV_OK=false

    if [[ -x "$VENV_PYTHON" ]]; then
        VENV_VERSION=$("$VENV_PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
        if [[ "$VENV_VERSION" == "$PYTHON_VERSION" ]]; then
            VENV_OK=true
        else
            echo "Existing venv uses Python $VENV_VERSION, but system has $PYTHON_VERSION — rebuilding."
        fi
    else
        echo "Existing venv has no usable python binary — rebuilding."
    fi

    if [[ "$VENV_OK" == false ]]; then
        echo "Removing $VENV_DIR ..."
        rm -rf "$VENV_DIR"
    fi
fi

# ── 5. Create venv if missing ─────────────────────────────────────────────────
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR"
    echo "Created: $VENV_DIR"
fi

# ── 6. Install / upgrade dependencies ────────────────────────────────────────
echo ""
echo "Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip --quiet
"$VENV_DIR/bin/pip" install -r "$REQUIREMENTS"

echo ""
echo "=== Setup complete ==="
echo ""
echo "To launch the app, run:"
echo "  ./launch.sh"
