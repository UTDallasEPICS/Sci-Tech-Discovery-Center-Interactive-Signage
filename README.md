# Sci-Tech-Discovery-Center-Interactive-Sinage


  

  

## Conceptual Overview

  

  

This project is an interactive signage system designed to run on a Raspberry Pi.

  

  

It allows users to scan an organ (Embedded with an NFC ID), via an NFC reader, and select a language using physical buttons. Based on the scanned ID and selected language, the system plays a specific educational video on screen.

  

  

Note : This project has mock videos and is to be replaced with actual educational videos in the future.

  

  

  

  

### ********Roles:********

  

  

-> ****_User:_**** Scans ID, selects language, watches video.

  

  

-> ****_Administrator:_*_**** Manually manages the video content and ID mappings via the JSON file (interactive-signage-backend/polls/testdata.json) and File system (artifacts directory containing video files)

  
  ### User Flow:
  Child scans an artifact --> Screen switches from the splash screen to language selection screen --> Child either presses a button for language selection within 15 seconds or waits --> Screen switches to video display screen and video plays (video is in language of button selection or defaults to English) --> Video ends --> Screen reverts to Splash Screen

  

  

  

### Functional Requirements

  

  

****Splash Screen:**** Contains "Scan here" message alongside a visual use diagram.

  

  

|- ****NFC Reader****: Reads NFC the ID via PN532 HAT, recognizes the ID, and switches to the language screen

  

  

****Language Selection Screen:****

  

  

|-Allows users to choose a language (English, Spanish, Telugu) via 3 physical buttons in a timeout period.

  

  

****Timeout Logic:**** Automatically defaults to English if no language is selected within 15 seconds.

  

  

|-****Video Playback****: Retrieves and plays the correct video file based on the selected ID and language.

  

  

|-****System Reset****: Returns to splash screen after video completion, to serve the next user.

  

  

  

  

****Real-time:**** Server-Sent Events (SSE) used to update the frontend state immediately upon the user's interaction.

  

  

  

  

### Third-Party Integrations

  

  

N/A - This is a fully self-contained system.

  

  

  

  

### Hardware Integration:

  

Enable ****SPI Interface**** on Raspberry Pi:

Open the terminal and run the configuration tool:

```bash sudo raspi-config ```

Navigate to ****Interfacing Options**** -> ****SPI**** -> ****Yes**** to enable the interface.

  

For more information visit: https://www.waveshare.com/wiki/PN532_NFC_HAT

Document on wiring is uploaded on EduSourced ****"Raspberry Pi Wiring Instructions"****

  

PN532 NFC HAT - Reads NFC cards via GPIO/SPI on Raspberry Pi

  

  

Physical Buttons - 3 buttons connected to GPIO pins for language selection

  

  

  

  

### Tech Stack

  

  

Frontend: React( + React Router) + Vite

  

  

Backend: Django (Python) + SSE

  

  

Hardware: Raspberry Pi + PN532 NFC HAT + GPIO Buttons

  

  

Storage:  JSON + Local Video Files

  

  

  

  

## First time setup:

  

  

  

  

##### (Download and Unpack the file. Your file structure should be like this)

  

  

  

  

Sci-Tech-Discovery-Center-Interactive-Sinage

  

  

├── frontend

  

  

├── Hardware_Layer

  

  

├── interactive-signage-backend

  

  

  

  

__**In file explorer when you unpack this, Copy its full path for reference**__

  

  

## 1. Hardware Layer Setup

  

Located in `Hardware_Layer/`.

  

```bash
cd path/to/your/directory/Sci-Tech-Discovery-Center-Interactive-Sinage-main
```

  

  

_*___When you run the command 'tree -L 1', you should see the files listed as the diagram above__*

  

  

1. Navigate to the specific directory:

  

  

```bash
cd Hardware_Layer
```

  

  

2.  Create and activate the virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

  

  

__**NOTE: python -m venv venv is used only once**__

  

  

3.  Install dependencies:

```bash
pip install requests adafruit-circuitpython-pn532 rpi-lgpio
```

  

  

4.  Run the hardware control script:

  

  

```bash
python ButtonPress_Updated.py & python UIDRead_Updated.py
```

  

  

## 2. Backend Setup

  

  

Located in `interactive-signage-backend/`.

  

  

  

  

1.  Navigate to the directory on a new terminal :

  

  

```bash
cd interactive-signage-backend
```

  

  

2.  Create (First time only) and activate the virtual environment:

  

  

```bash
python -m venv venv
source venv/bin/activate
```

  

  

3.  Install dependencies:

  

  

```bash
pip install -r requirements.txt
```

  

  

  

4. Generate a secret key. Copy the terminal output and add this to your .env file:

  

  

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

  

  

  

  

Use nano .env to open and edit the .env file. Change the key variable and add in your generated key.

  

  

SECRET_KEY='<your-generated-secret-key-goes-here>'

  

  

  

Save and exit nano

  

  

  

  

5.  Start the Django server:

  

  

  

  

```bash
python manage.py runserver
```

  

  

The server will start at the assigned IP given.

  

  

  

  

## 3. Frontend Setup

  

Located in `frontend/`.

  

No additional steps are required as running the backend server will start the frontend

  

  

  

  

  

  

## 4. Running the App

  

  

- Ensure the Hardware Layer scripts are running in a separate terminal to allow button press and id scanning.

  

  

- Access the application at *http://localhost:8000/*.

  

  

  

  

## 5. Termination

  

  

__**As the scripts are running, you cannot run other commands.**__

  

  

Terminate the script at the respective terminals using the 'Ctrl+C' combination. You should be able to see this in the terminal and run other commands like normal.

  

  

```bash
C^
```

  

  

  

__**Note: set DEBUG = false when this project is deployed for production**__
