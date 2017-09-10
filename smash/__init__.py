#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

from smash.setup.arguments import __version__

from .__main__ import console
from .__main__ import main

from .cmdline import parse as parse_cmdline

from .sys.config import Config
from .sys.config import ConfigTree

from .sys.exporter import Exporter
from .sys.exporter import ExportDebug
from .sys.exporter import ExportShell

from .sys.handler import *

from .utils.out import debuglog
from .utils.out import loggers_for



#----------------------------------------------------------------------#

