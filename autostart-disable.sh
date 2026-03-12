#!/bin/bash
# ============================================================
#  Disable auto-start on boot.
# ============================================================

echo "Disabling auto-start..."

# Remove labwc autostart entry
LABWC_FILE="$HOME/.config/labwc/autostart"
if [ -f "$LABWC_FILE" ]; then
    grep -v "# Sci-Tech Signage" "$LABWC_FILE" | grep -v "start.sh" > "$LABWC_FILE.tmp"
    mv "$LABWC_FILE.tmp" "$LABWC_FILE"
    echo "  Removed from labwc autostart."
fi

# Remove XDG .desktop file
XDG_FILE="$HOME/.config/autostart/signage.desktop"
if [ -f "$XDG_FILE" ]; then
    rm "$XDG_FILE"
    echo "  Removed XDG autostart entry."
fi

echo ""
echo "Auto-start disabled. The kiosk will no longer launch on boot."
