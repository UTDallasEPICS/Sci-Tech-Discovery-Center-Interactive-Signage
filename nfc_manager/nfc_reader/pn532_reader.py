import time
from .base import BaseNFCReader


class PN532NFCReader(BaseNFCReader):
    """Hardware NFC Reader using the PN532 HAT over SPI (same hardware as the signage kiosk)."""

    def __init__(self, reset_pin=20, cs_pin=4):
        super().__init__()
        try:
            from pn532 import PN532_SPI
            self.pn532 = PN532_SPI(debug=False, reset=reset_pin, cs=cs_pin)
            ic, ver, rev, support = self.pn532.get_firmware_version()
            print(f"PN532 firmware version: {ver}.{rev}")
            self.pn532.SAM_configuration()
        except Exception as e:
            raise ImportError(f"Failed to initialize PN532: {e}")

    def _run_loop(self):
        """Poll the PN532 for NFC tags, matching the signage project's UID format."""
        last_uid = None
        last_scan_time = 0

        while self._running:
            try:
                uid = self.pn532.read_passive_target(timeout=0.5)
                if uid is None:
                    continue

                current_time = time.time()

                # Debounce: same tag within 3 seconds is ignored
                if uid == last_uid and (current_time - last_scan_time) < 3:
                    continue

                # Convert 7-byte UID to decimal string, matching signage format
                if len(uid) == 7:
                    decimal_id = str(int.from_bytes(uid, byteorder='big'))
                else:
                    decimal_id = str(int.from_bytes(uid, byteorder='big'))

                last_uid = uid
                last_scan_time = current_time

                if self.on_tag_scanned_callback:
                    self.on_tag_scanned_callback(decimal_id)

            except Exception as e:
                print(f"PN532 read error: {e}")

            time.sleep(0.1)
