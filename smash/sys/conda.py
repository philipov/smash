#-- smash.env.conda

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
from .env import environment

#----------------------------------------------------------------------#

class CondaEnvironment(VirtualEnvironment):
    pass

@contextmanager
def subenv( *args, **kwargs ) -> CondaEnvironment :
    '''run a subordinate environment using conda'''
    with environment( *args, envclass_=CondaEnvironment, **kwargs ) as e :
        yield e


#----------------------------------------------------------------------#
