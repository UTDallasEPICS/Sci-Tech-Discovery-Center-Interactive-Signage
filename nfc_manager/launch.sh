#!/usr/bin/env bash
# launch.sh — Start the NFC Tag Manager
# Automatically runs setup if the virtual environment is missing or broken.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# ── Validate venv ─────────────────────────────────────────────────────────────
NEEDS_SETUP=false

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Virtual environment not found or broken — running setup..."
    NEEDS_SETUP=true
else
    # Check that venv python matches system python version
    SYS_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "")
    VENV_VERSION=$("$VENV_PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "")

    if [[ -z "$VENV_VERSION" || "$SYS_VERSION" != "$VENV_VERSION" ]]; then
        echo "Virtual environment is stale (Python $VENV_VERSION vs system $SYS_VERSION) — running setup..."
        NEEDS_SETUP=true
    fi
fi

if [[ "$NEEDS_SETUP" == true ]]; then
    bash "$SCRIPT_DIR/setup.sh"
    echo ""
fi

# ── Launch ────────────────────────────────────────────────────────────────────
echo "Starting NFC Tag Manager..."
cd "$SCRIPT_DIR"
exec "$VENV_PYTHON" main.py "$@"
