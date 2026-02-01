from . import version
from rich import traceback

traceback.install(show_locals=False)

__version__ = version.__version__
