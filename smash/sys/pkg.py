#-- smash.sys.pkg

"""
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path
from contextlib import contextmanager

__all__ = []

import conda
from .env import VirtualEnvironment


#----------------------------------------------------------------------#

class Package:
    pass



#----------------------------------------------------------------------#
