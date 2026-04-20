# NFC Tag Manager

A desktop application designed to pair NFC tags with corresponding media files. This tool is built specifically to make assigning videos to organ NFC tags intuitive and user-friendly.

## Prerequisites
- Python 3.9+
- macOS, Linux, or Windows

## Setup Instructions

1. **Activate the Virtual Environment**:
   Before running the app, you need to load the local Python environment that contains the required libraries.
   ```bash
   source .venv/bin/activate
   ```
   *(If the virtual environment is ever broken due to the folder being moved, you can rebuild it by running `rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`)*

2. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage
- **Simulating Scans**: When developing on macOS or Windows, a "Dev: Simulate Scan" panel will appear on the bottom left. Enter any arbitrary UID (e.g., `LIVER-001`) and click "Simulate" to act as if a tag was just tapped.
- **Adding/Editing Tags**: Upon scanning a tag, a modal will appear prompting you to enter the Organ's Name and select its Video File. The video will be copied to the `media/` directory, and the relationships will be saved to `tags.json`.

## Brand Styling
The GUI is built using `customtkinter` with elements conforming to the brand guidelines (Purple primary, Orange/Yellow accents, and specialized fonts).
