#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""


from .constants import __version__
from .constants import __setup__
from .constants import __test_setup__

#----------------------------------------------------------------------#

from .cmdline import parse as parse_cmdline

from .__main__ import main
from .__main__ import console

from .sys.config import Config
from .sys.config import ConfigTree

from .sys.export import Exporter
from .sys.export import ExportDebug
from .sys.export import ExportEnvironment

from .utils.out import debuglog
from .utils.out import loggers_for


#----------------------------------------------------------------------#

from .sys.plugins import plugins


#----------------------------------------------------------------------#

