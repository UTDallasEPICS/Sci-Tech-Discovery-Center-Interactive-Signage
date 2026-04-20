import os
import sys
from data.manager import DataManager
from gui.app import App


def get_nfc_reader():
    """Select NFC reader: PN532 hardware on Pi, mock on dev machines."""
    if sys.platform in ['darwin', 'win32'] or os.environ.get('USE_MOCK_READER') == '1':
        print("Using Mock NFC Reader for development.")
        from nfc_reader.mock_reader import MockNFCReader
        return MockNFCReader()
    else:
        try:
            from nfc_reader.pn532_reader import PN532NFCReader
            print("Using PN532 NFC Reader.")
            return PN532NFCReader()
        except ImportError as e:
            print(f"Failed to load PN532 reader: {e}. Falling back to Mock Reader.")
            from nfc_reader.mock_reader import MockNFCReader
            return MockNFCReader()


def main():
    # Load brand theme
    import customtkinter as ctk
    theme_path = os.path.join(os.path.dirname(__file__), 'gui', 'theme.json')
    if os.path.exists(theme_path):
        ctk.set_default_color_theme(theme_path)

    # Initialize DataManager with config pointing to signage project
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    data_manager = DataManager(config_path=config_path)

    nfc_reader = get_nfc_reader()

    # Start background reader thread
    nfc_reader.start()

    # Initialize and run GUI
    app = App(data_manager=data_manager, nfc_reader=nfc_reader)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        nfc_reader.stop()


if __name__ == "__main__":
    main()
