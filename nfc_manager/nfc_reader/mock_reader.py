from .base import BaseNFCReader

class MockNFCReader(BaseNFCReader):
    """A mock NFC reader for testing on macOS without physical hardware."""
    
    def __init__(self):
        super().__init__()
        
    def _run_loop(self):
        """Mock reader doesn't need a background thread loop for reading,
        interaction will happen via the simulate_scan method."""
        pass
        
    def simulate_scan(self, uid: str):
        """Simulate scanning an NFC tag."""
        if self.on_tag_scanned_callback:
            self.on_tag_scanned_callback(uid)
