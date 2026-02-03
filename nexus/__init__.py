from . import version
from rich import traceback

from nexus.core import VariableLibrary

traceback.install(show_locals=VariableLibrary.get_variable("exceptions.show_locals"))

__version__ = version.__version__
