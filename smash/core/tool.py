#-- smash.core.tool

"""
isolate changes to the state of an environment so they can be tracked and versioned
"""

import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

from pathlib import Path
from .config import Config

from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from ..util.meta import classproperty
from powertools import export


#----------------------------------------------------------------------#

@export
class Subprocess:
    ''' Base class for creating wrappers to keep track of state manipulation '''


    def __init__( self, environment ) :
        self.environment = environment

    def command( self, platform ) :
        return str( self )

    def command_windows(self):
        raise NotImplementedError

    def command_linux(self):
        raise NotImplementedError

    def command_mac(self):
        raise NotImplementedError



#----------------------------------------------------------------------#

@export
class Task( Subprocess ) :
    ''' perform an action once '''



    def command_windows( self ) :
        raise NotImplementedError

    def command_linux( self ) :
        raise NotImplementedError

    def command_mac( self ) :
        raise NotImplementedError

#----------------------------------------------------------------------#

@export
class Installer( Subprocess ) :
    ''' install external dependencies using their own script '''

@export
class MinicondaInstaller( Installer ):
    ''' python '''

    def command_windows(self):
        return ''

    def command_linux( self ) :
        return ''

#----------------------------------------------------------------------#

@export
class Loader( Task ) :
    ''' batch job for writing to a data store '''


@export
class Validator( Task ) :
    ''' a task that checks whether a previous task succeeded and records the result '''


################################
@export
class Daemon( Subprocess ) :
    ''' until killed: start a subprocess, block until it terminates, then repeat '''

@export
class Service( Daemon ) :
    ''' pass '''

@export
class Monitor( Daemon ) :
    ''' pass '''


#----------------------------------------------------------------------#

builtin_tools = {
    'Task'      : Task,
    'Loader'    : Loader,
    'Validator' : Validator,

    'Daemon'    : Daemon,
    'Monitor'   : Monitor,
    'Service'   : Service,
}



#----------------------------------------------------------------------#
