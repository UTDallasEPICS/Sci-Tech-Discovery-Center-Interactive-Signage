__all__ = [
    'pn532',
    'spi',
    'PN532_SPI',
]

from . import pn532
from .spi import PN532_SPI

# Optional transports — only available if their dependencies are installed.
try:
    from .i2c import PN532_I2C
    __all__ += ['i2c', 'PN532_I2C']
except ImportError:
    pass

try:
    from .uart import PN532_UART
    __all__ += ['uart', 'PN532_UART']
except ImportError:
    pass
