#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

from smash.sys.constants import __setup__
from smash.sys.constants import __test_setup__
from smash.sys.constants import __version__

from .__main__ import console
from .__main__ import main
from .cmdline import parse as parse_cmdline
from .sys.config import Config
from .sys.config import ConfigTree
from .sys.export import ExportDebug
from .sys.export import ExportShell
from .sys.export import Exporter
from .sys.plugins import plugins
from .utils.out import debuglog
from .utils.out import loggers_for



#----------------------------------------------------------------------#

