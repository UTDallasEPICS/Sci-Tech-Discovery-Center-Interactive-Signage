# Legacy compatibility — redirect to PN532 reader
from .pn532_reader import PN532NFCReader as PiNFCReader

__all__ = ["PiNFCReader"]
