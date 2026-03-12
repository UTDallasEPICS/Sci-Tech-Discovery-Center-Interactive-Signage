#!/bin/bash
# ============================================================
#  Sci-Tech Discovery Center Interactive Signage — Stop
#  Stops all running services.
# ============================================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Stopping all signage services..."

if [ -f "$PROJECT_DIR/.pids" ]; then
    while read -r pid; do
        kill "$pid" 2>/dev/null
    done < "$PROJECT_DIR/.pids"
    rm -f "$PROJECT_DIR/.pids"
fi

# Belt-and-suspenders: kill by process name
pkill -f "manage.py runserver" 2>/dev/null
pkill -f "UIDRead_Updated.py" 2>/dev/null
pkill -f "ButtonPress_Updated.py" 2>/dev/null

echo "Done."
