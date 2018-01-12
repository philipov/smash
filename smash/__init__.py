#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

from smash.__setup__ import __version__

from .__main__ import console


from .core.yamlisp import YAMLispNode
from .core.yamlisp import BoxTree


from .core.env import *

from .core.exporter import *
from .core.tool import *

from .core import plugin

from .core.plugin import environment_types

from .core.plugin import tools
from .core.plugin import exporters

from .core import platform


#----------------------------------------------------------------------------------------------#

