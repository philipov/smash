#-- smash.sys.env

"""
environment management
"""


import logging

log = logging.getLogger( name="smash.sys.env" )
logging.basicConfig( level=logging.DEBUG )
log.debug = print
# log.debug = lambda *a, **b : None

################################
from pathlib import Path

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj

#----------------------------------------------------------------------#

def register_script_to_context_menu( ) :
    # http://support.microsoft.com/kb/310516
    cmd_line = 'regedit.exe registerOne.reg'
    import os
    os.system( cmd_line )

#----------------------------------------------------------------------#

def install_configsystem( install_root: Path, force=False ) :
    if install_root.exists( ) :
        # todo: make backup
        pass

#----------------------------------------------------------------------#
