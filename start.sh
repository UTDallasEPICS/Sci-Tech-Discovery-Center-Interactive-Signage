#!/bin/bash
# ============================================================
#  Sci-Tech Discovery Center Interactive Signage — Start
#  Starts the web server, NFC reader, and button listener.
#  Press Ctrl+C to stop everything (when run from a terminal).
# ============================================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGFILE="$PROJECT_DIR/signage.log"
PIDS=()

# If not running in a terminal (e.g., launched by autostart), redirect all
# output to a log file so errors aren't silently lost.
if [ ! -t 1 ]; then
    exec > "$LOGFILE" 2>&1
    echo "=== Signage autostart at $(date) ==="
    # Give the desktop and network a moment to finish loading.
    sleep 5
fi

cleanup() {
    echo ""
    echo "Stopping all services..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done
    pkill -f "manage.py runserver" 2>/dev/null
    pkill -f "UIDRead_Updated.py" 2>/dev/null
    pkill -f "ButtonPress_Updated.py" 2>/dev/null
    rm -f "$PROJECT_DIR/.pids"
    echo "All services stopped."
    exit 0
}

trap cleanup SIGINT SIGTERM

echo ""
echo "=========================================="
echo "  Interactive Signage — Starting Up"
echo "=========================================="
echo ""

# --- Preflight checks ---

if [ ! -d "$PROJECT_DIR/interactive-signage-backend/venv" ]; then
    echo "ERROR: Backend not set up. Run ./setup.sh first."
    exit 1
fi

if [ ! -d "$PROJECT_DIR/frontend/dist" ]; then
    echo "ERROR: Frontend not built. Run ./setup.sh first."
    exit 1
fi

# --- Start Django web server ---

echo "Starting web server..."
cd "$PROJECT_DIR/interactive-signage-backend"
"$PROJECT_DIR/interactive-signage-backend/venv/bin/python3" manage.py runserver 0.0.0.0:8000 2>&1 &
PIDS+=($!)
echo "  Web server started (http://localhost:8000)"

# Wait for server to come up
sleep 3

# --- Start hardware scripts (only on a Raspberry Pi) ---

if [ -e "/dev/spidev0.0" ]; then
    echo "Starting NFC reader..."
    cd "$PROJECT_DIR/Hardware_Layer"
    "$PROJECT_DIR/Hardware_Layer/venv/bin/python3" UIDRead_Updated.py 2>&1 &
    PIDS+=($!)
    echo "  NFC reader started."

    echo "Starting button listener..."
    "$PROJECT_DIR/Hardware_Layer/venv/bin/python3" ButtonPress_Updated.py 2>&1 &
    PIDS+=($!)
    echo "  Button listener started."
else
    echo ""
    echo "  NOTE: SPI not detected — skipping NFC reader and button scripts."
    echo "  (This is normal if you are not running on a Raspberry Pi.)"
    echo "  On the Pi, language buttons on the touchscreen still work."
fi

# Save PIDs for stop.sh
printf "%s\n" "${PIDS[@]}" > "$PROJECT_DIR/.pids"

# --- Open browser in kiosk mode (Pi with desktop only) ---

sleep 1
if command -v chromium-browser &> /dev/null; then
    echo ""
    echo "Opening browser in kiosk mode..."
    chromium-browser \
        --kiosk \
        --noerrdialogs \
        --disable-infobars \
        --disable-restore-session-state \
        --disable-session-crashed-bubble \
        --password-store=basic \
        http://localhost:8000 &
fi

echo ""
echo "=========================================="
echo "  System is running."
echo "  Press Ctrl+C to stop."
echo "=========================================="
echo ""

# Keep running until Ctrl+C
wait
