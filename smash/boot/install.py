#-- smash.env.virtual

"""
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path

__all__ = []

#----------------------------------------------------------------------#

def create_instance(instance_root:Path):
    '''create '''

    yield
    #teardown


#----------------------------------------------------------------------#

def install_configsystem( install_root: Path, force=False ) :
    if install_root.exists( ) :
        # todo: make backup
        pass
