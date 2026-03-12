# Sci-Tech Discovery Center — Interactive Signage

An interactive kiosk for the Human Machine exhibit. A child scans a body-part
artifact on the NFC reader, picks a language, and watches a short educational
video — then the screen resets for the next visitor.

**Supported languages:** English, Spanish (Español), Telugu


---

## How It Works

```
Child scans artifact  ➜  Language selection screen  ➜  Video plays  ➜  Back to start
       (NFC)             (buttons or touchscreen)       (auto-play)
```

1. **Splash screen** — displays "Scan Here" with a picture of how to scan.
2. **NFC scan** — the child holds an organ artifact (with an embedded NFC tag)
   near the reader. The screen switches to language selection.
3. **Language selection** — three physical buttons (or on-screen buttons) let the
   child choose English, Spanish, or Telugu. If no button is pressed within
   15 seconds, English is chosen automatically.
4. **Video playback** — the matching video plays full-screen.
5. **Reset** — when the video ends, the screen returns to step 1.


---

## What You Need

### Hardware

| Item | Notes |
|------|-------|
| Raspberry Pi 5 | With power supply and microSD card (32 GB+) |
| PN532 NFC HAT | Waveshare — plugs directly onto the Pi GPIO header |
| 3 push buttons | For language selection (English / Spanish / Telugu) |
| Display | Any monitor or TV with HDMI input |
| Jumper wires | To connect buttons to the GPIO header |

### Software

Everything is installed automatically by the setup script. For reference:

- **Raspberry Pi OS** (Bookworm, 64-bit) — the standard Pi operating system
- **Python 3.11+** — comes with Pi OS
- **Node.js** — installed during setup, used to build the on-screen display
- **Django** — Python web server (backend)
- **React + Vite** — on-screen interface (frontend)


---

## Setup Guide (One Time)

### Step 1 — Install Raspberry Pi OS

1. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to
   flash **Raspberry Pi OS (64-bit)** onto a microSD card.
2. Boot the Pi, connect to Wi-Fi, and finish the first-time setup wizard.
3. Open a terminal (the black icon in the taskbar).

### Step 2 — Enable the SPI Interface

The NFC hat communicates over SPI, which is off by default.

```bash
sudo raspi-config
```

Navigate with the arrow keys:

```
Interface Options  ➜  SPI  ➜  Yes  ➜  Finish
```

Reboot when prompted:

```bash
sudo reboot
```

### Step 3 — Download the Project

After rebooting, open a terminal and run:

```bash
cd ~/Desktop
git clone https://github.com/UTDallasEPICS/Sci-Tech-Discovery-Center-Interactive-Signage.git
cd Sci-Tech-Discovery-Center-Interactive-Signage
```

### Step 4 — Run the Setup Script

This single command installs all dependencies and builds the display:

```bash
./setup.sh
```

The script will:
- Install system packages (Node.js, Python venv tools)
- Create isolated Python environments for the backend and hardware layer
- Install all Python and JavaScript dependencies
- Build the frontend
- Generate a secret key
- Verify that SPI is enabled

**This takes 5–10 minutes on a Pi 5.** You will see progress as it runs.
If you see any red error text, read the message — it will tell you what to fix.

### Step 5 — Wire the Buttons

The NFC hat plugs directly onto the Pi's 40-pin GPIO header — no soldering
needed. The three language buttons connect to the hat's pass-through pins:

```
Button          GPIO Pin    Physical Pin    Wire to
──────────────  ──────────  ──────────────  ────────────────
English         GPIO 17     Pin 11          3.3V (Pin 1 or 17)
Spanish         GPIO 27     Pin 13          3.3V (Pin 1 or 17)
Telugu          GPIO 22     Pin 15          3.3V (Pin 1 or 17)
```

For each button:
- Connect one leg to the **GPIO pin** listed above.
- Connect the other leg to **3.3V** (any of Pin 1 or Pin 17 on the header).
- The software uses internal pull-down resistors, so no external resistors are
  needed.

> For detailed wiring photos, see the document "Raspberry Pi Wiring
> Instructions" uploaded on EduSourced.


---

## Starting and Stopping

### Start

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage
./start.sh
```

This starts the web server, NFC reader, and button listener, then opens
Chromium in kiosk mode (full-screen, no browser controls).

### Stop

Press **Ctrl+C** in the terminal where `start.sh` is running.

Or, from any terminal:

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage
./stop.sh
```


---

## Auto-Start on Boot (Optional)

To make the kiosk start automatically every time the Pi is powered on:

1. Open a terminal and create an autostart entry:

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/signage.desktop
```

2. Paste the following (change the path if you put the project somewhere other
   than `~/Desktop`):

```ini
[Desktop Entry]
Type=Application
Name=Sci-Tech Signage
Exec=/home/pi/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage/start.sh
X-GNOME-Autostart-enabled=true
```

3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

4. Reboot to test:

```bash
sudo reboot
```

The system should start on its own after the desktop loads.

To **disable** auto-start, delete the file:

```bash
rm ~/.config/autostart/signage.desktop
```


---

## Managing Content

### Video Files

Videos are stored in `frontend/public/artifacts/`. Each organ has a folder
with one video per language:

```
frontend/public/artifacts/
├── heart/
│   ├── en.mp4      (English)
│   ├── es.mp4      (Spanish)
│   └── te.mp4      (Telugu)
├── brain/
│   ├── en.mp4
│   ├── es.mp4
│   └── te.mp4
├── lungs/
│   ...
```

**To replace a video:** drop the new `.mp4` file into the correct folder with
the correct name (`en.mp4`, `es.mp4`, or `te.mp4`), replacing the old one.

**After changing any videos, rebuild the frontend:**

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage/frontend
npx vite build
```

Then restart the system (`./stop.sh` then `./start.sh`).

### Adding a New Organ

1. Create a new folder under `frontend/public/artifacts/` (e.g., `stomach/`)
   and put the three videos inside (`en.mp4`, `es.mp4`, `te.mp4`).

2. Find the NFC tag's ID by scanning it and checking the terminal output of
   `UIDRead_Updated.py` — it prints the decimal ID.

3. Edit `interactive-signage-backend/polls/testdata.json` and add a new entry:

```json
{
    "id": "YOUR_NFC_TAG_DECIMAL_ID",
    "name": "stomach",
    "path": {
        "en": "artifacts/stomach/en.mp4",
        "es": "artifacts/stomach/es.mp4",
        "te": "artifacts/stomach/te.mp4"
    }
}
```

4. Rebuild the frontend and restart:

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage/frontend
npx vite build
cd ..
./stop.sh
./start.sh
```

### Current Organs

| Organ | NFC Tag ID |
|-------|-----------|
| Heart | 1212866967841409 |
| Brain | 1356877221276289 |
| Lungs | 1200652064074369 |
| Liver | 1303980387281537 |
| Kidneys | 1371020531804801 |
| Intestines | 1201708626029185 |
| Skin | 1320988474550913 |
| Artery | 1275423149730433 |
| Vein | 1154575671700097 |
| Nerves | 1270045867453057 |


---

## Troubleshooting

### "No video plays" or black screen on the video page

- Make sure you rebuilt the frontend after adding or changing videos:
  ```bash
  cd frontend && npx vite build
  ```
- Check that the video file exists at the expected path (e.g.,
  `frontend/dist/artifacts/heart/en.mp4`).

### NFC scanning does not work

- Verify SPI is enabled: `ls /dev/spidev*` should show `/dev/spidev0.0`.
  If not, run `sudo raspi-config` and enable SPI under Interface Options.
- Make sure the PN532 HAT is seated firmly on the GPIO header.
- Check the terminal output of `start.sh` for error messages from the NFC
  reader.

### Buttons do not respond

- Verify wiring: each button should connect a GPIO pin (17, 27, or 22) to
  3.3V when pressed.
- Check the terminal output — button presses are logged when detected.
- The **on-screen buttons also work** as a fallback if the physical buttons
  have an issue.

### Second scan does not work (stuck after first video)

This was a bug in earlier versions. If you are seeing this, make sure you are
running the latest code. Pull the latest changes:

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage
git pull
./setup.sh
```

### "Command not found" errors during setup

Make sure you are in the correct directory:

```bash
cd ~/Desktop/Sci-Tech-Discovery-Center-Interactive-Signage
```

### "Externally managed environment" error from pip

This is normal on newer Pi OS versions. The setup script avoids this by using
virtual environments. Do **not** run `pip install` directly — always use
`./setup.sh`.

### Browser does not open automatically

If Chromium does not launch, open it manually and go to
`http://localhost:8000`. To go full-screen, press `F11`.

### The screen is not in kiosk mode / shows browser controls

Press `F11` to toggle full-screen in Chromium, or close it and re-run
`./start.sh` which opens Chromium in kiosk mode automatically.


---

## Project Structure

```
Sci-Tech-Discovery-Center-Interactive-Signage/
│
├── setup.sh                        ← Run once to install everything
├── start.sh                        ← Start the kiosk
├── stop.sh                         ← Stop the kiosk
│
├── frontend/                       ← On-screen interface (React)
│   ├── src/                        ← Source code
│   ├── public/artifacts/           ← Video files (edit these)
│   └── dist/                       ← Built output (auto-generated)
│
├── interactive-signage-backend/    ← Web server (Django)
│   ├── polls/
│   │   ├── views.py                ← API endpoints
│   │   ├── getpath.py              ← Video path lookup
│   │   └── testdata.json           ← NFC ID → video mapping
│   └── mysite/
│       └── settings.py             ← Server configuration
│
└── Hardware_Layer/                 ← Raspberry Pi hardware scripts
    ├── UIDRead_Updated.py          ← NFC tag reader
    ├── ButtonPress_Updated.py      ← Physical button listener
    └── pn532/                      ← NFC hat driver library
```


---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Display | React 19 + Vite + Tailwind CSS |
| Server | Django 5 (Python) with Server-Sent Events |
| Hardware | PN532 NFC HAT (SPI) + GPIO push buttons |
| Communication | REST API + SSE for real-time updates |
| Storage | JSON config file + local .mp4 video files |


---

## For Developers

### Architecture

```
 ┌────────────────┐      HTTP       ┌──────────────────┐     SSE      ┌──────────────┐
 │  NFC Reader    │ ──────────────► │                  │ ◄──────────► │              │
 │  (Python)      │  /api/receive-  │  Django Server   │  /api/events │  React App   │
 │                │      id/        │  (port 8000)     │              │  (browser)   │
 ├────────────────┤                 │                  │              │              │
 │  Button Script │ ──────────────► │                  │ ───────────► │              │
 │  (Python)      │  /api/receive-  │                  │  /api/       │              │
 │                │      button/    │                  │  showinfo    │              │
 └────────────────┘                 └──────────────────┘              └──────────────┘
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/receive-id/?id=<id>` | GET | Register an NFC scan |
| `/api/receive-button/?button=a\|b\|c` | GET | Register a language button press (a=EN, b=ES, c=TE) |
| `/api/showinfo/` | GET | Get the video path for the current scan + language |
| `/api/resetinfo/` | GET | Reset state for the next visitor |
| `/api/events/` | GET | SSE stream — pushes `scanned_id`, `button_press`, `button_press_timeout` events |

### Running in Development (not on a Pi)

You can run just the backend and frontend on any machine for UI development.
The hardware scripts are skipped automatically when SPI is not available, and
the on-screen language buttons work without physical buttons.

```bash
# Terminal 1 — backend
cd interactive-signage-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

# Terminal 2 — frontend (with hot reload)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173` (Vite dev server) or `http://localhost:8000`
(Django serving the built frontend).

You can simulate an NFC scan with curl:

```bash
curl "http://localhost:8000/api/receive-id/?id=1212866967841409"
```

And simulate a button press:

```bash
curl "http://localhost:8000/api/receive-button/?button=a"
```
