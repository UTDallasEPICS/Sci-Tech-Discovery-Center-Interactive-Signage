#!/bin/bash
# ============================================================
#  Enable auto-start on boot.
#  Works on Raspberry Pi OS Bookworm (labwc/Wayland) and
#  older versions (LXDE/X11).
# ============================================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
START_SCRIPT="$PROJECT_DIR/start.sh"

if [ ! -f "$START_SCRIPT" ]; then
    echo "ERROR: start.sh not found at $START_SCRIPT"
    exit 1
fi

echo "Setting up auto-start on boot..."
echo ""

INSTALLED=false

# --- Method 1: labwc autostart (Bookworm Pi 5 default) ---
LABWC_DIR="$HOME/.config/labwc"
if [ -d "$LABWC_DIR" ] || command -v labwc &> /dev/null; then
    mkdir -p "$LABWC_DIR"
    LABWC_FILE="$LABWC_DIR/autostart"

    # Remove any existing signage entry, then append
    if [ -f "$LABWC_FILE" ]; then
        grep -v "# Sci-Tech Signage" "$LABWC_FILE" | grep -v "start.sh" > "$LABWC_FILE.tmp"
        mv "$LABWC_FILE.tmp" "$LABWC_FILE"
    fi

    echo "# Sci-Tech Signage — auto-start kiosk" >> "$LABWC_FILE"
    echo "$START_SCRIPT &" >> "$LABWC_FILE"
    chmod +x "$LABWC_FILE"

    echo "  Added to labwc autostart: $LABWC_FILE"
    INSTALLED=true
fi

# --- Method 2: XDG autostart .desktop file (fallback for X11/LXDE) ---
XDG_DIR="$HOME/.config/autostart"
mkdir -p "$XDG_DIR"
cat > "$XDG_DIR/signage.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Sci-Tech Signage
Exec=$START_SCRIPT
X-GNOME-Autostart-enabled=true
EOF

echo "  Added XDG autostart: $XDG_DIR/signage.desktop"
INSTALLED=true

if $INSTALLED; then
    echo ""
    echo "Auto-start enabled. The kiosk will launch after the next reboot."
    echo ""
    echo "  To test now:    ./start.sh"
    echo "  To reboot:      sudo reboot"
    echo "  To disable:     ./autostart-disable.sh"
else
    echo ""
    echo "ERROR: Could not detect desktop environment."
    echo "       Auto-start was not configured."
    exit 1
fi
