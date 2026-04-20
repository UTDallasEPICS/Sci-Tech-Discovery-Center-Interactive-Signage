import threading
from typing import Callable, Optional

class BaseNFCReader:
    """Abstract base class for NFC readers."""

    def __init__(self):
        self.on_tag_scanned_callback: Optional[Callable[[str], None]] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def set_callback(self, callback: Callable[[str], None]):
        """Set the callback function to be called when a tag is scanned."""
        self.on_tag_scanned_callback = callback

    def start(self):
        """Start reading for NFC tags. Should be implemented by subclasses."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop reading for NFC tags."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None

    def _run_loop(self):
        """The main loop for reading tags. Subclasses should override this."""
        pass
