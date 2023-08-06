try:
    from chisel3.version import version as __version__
except ImportError:
    __version__ = "unknown"

from chisel3_jar import main
source = main.source
