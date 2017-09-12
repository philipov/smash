#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

from smash.setup.arguments import __version__

from .__main__ import console
from .__main__ import main

from .cmdline import parse as parse_cmdline

from .core.config import Config
from .core.config import ConfigTree

from .core.env import *
from .core.instance import *
from .core.pkg import *

from .core.exporter import *
from .core.handler import *
from .core.tool import *
from .core.user import *

from .core.plugins import *

from .core import platform


#----------------------------------------------------------------------#

