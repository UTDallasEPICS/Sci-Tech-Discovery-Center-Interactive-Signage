#!/bin/bash
# ============================================================
#  Sci-Tech Discovery Center Interactive Signage — Setup
#  Run this ONCE on a fresh Raspberry Pi to install everything.
# ============================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "=========================================="
echo "  Interactive Signage — First-Time Setup"
echo "=========================================="
echo ""

# --- Sanity checks ---

if [ "$(id -u)" -eq 0 ]; then
    echo -e "${RED}ERROR: Do not run this script as root (no sudo).${NC}"
    echo "       Run it as your normal Pi user:  ./setup.sh"
    exit 1
fi

if [ ! -d "$PROJECT_DIR/frontend" ] || [ ! -d "$PROJECT_DIR/interactive-signage-backend" ] || [ ! -d "$PROJECT_DIR/Hardware_Layer" ]; then
    echo -e "${RED}ERROR: Run this script from the project root directory.${NC}"
    echo "       Expected to find frontend/, interactive-signage-backend/, and Hardware_Layer/"
    exit 1
fi

# --- System packages ---

echo -e "${YELLOW}[1/5] Installing system packages...${NC}"
sudo apt update -qq
sudo apt install -y python3-venv python3-pip nodejs npm git
echo -e "${GREEN}  Done.${NC}"
echo ""

# --- Backend ---

echo -e "${YELLOW}[2/5] Setting up Django backend...${NC}"
cd "$PROJECT_DIR/interactive-signage-backend"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

venv/bin/python3 -m pip install --upgrade pip -q
venv/bin/python3 -m pip install -r requirements.txt -q

# Generate .env with a secret key if it doesn't exist
if [ ! -f ".env" ]; then
    SECRET=$(venv/bin/python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    echo "SECRET_KEY=$SECRET" > .env
    echo "  Generated new secret key in .env"
else
    echo "  .env already exists — keeping existing secret key."
fi

echo -e "${GREEN}  Backend ready.${NC}"
echo ""

# --- Hardware Layer ---

echo -e "${YELLOW}[3/5] Setting up hardware layer...${NC}"
cd "$PROJECT_DIR/Hardware_Layer"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

venv/bin/python3 -m pip install --upgrade pip -q
venv/bin/python3 -m pip install -r requirements.txt -q
echo -e "${GREEN}  Hardware layer ready.${NC}"
echo ""

# --- Frontend ---

echo -e "${YELLOW}[4/5] Building frontend (this may take a few minutes on the Pi)...${NC}"
cd "$PROJECT_DIR/frontend"

npm install --loglevel=error
npx vite build
echo -e "${GREEN}  Frontend built.${NC}"
echo ""

# --- SPI check ---

echo -e "${YELLOW}[5/5] Checking SPI interface...${NC}"
if [ -e "/dev/spidev0.0" ]; then
    echo -e "${GREEN}  SPI is enabled.${NC}"
else
    echo -e "${RED}  SPI is NOT enabled. The NFC hat will not work without it.${NC}"
    echo ""
    echo "  To enable SPI:"
    echo "    1. Run:  sudo raspi-config"
    echo "    2. Go to: Interface Options > SPI > Yes"
    echo "    3. Reboot the Pi"
    echo ""
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  Setup complete!${NC}"
echo "=========================================="
echo ""
echo "  To start the system:  ./start.sh"
echo ""
