#-- smash.sys.tools

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

from ..utils import out
from ..utils.out import rprint
from pprint import pprint, pformat

from ..utils.meta import classproperty
from powertools import export


#----------------------------------------------------------------------#

@export
class Tool:
    ''' Base class for creating wrappers to keep track of state manipulation '''

    def __init__( self, config:Config, filename:str, refname:str ) :
        self.config = config
        self.filename = filename
        self.refname = refname


#----------------------------------------------------------------------#

@export
class Task( Tool ) :
    ''' perform an action once '''


@export
class Loader( Task ) :
    ''' batch job for writing to a data store '''

@export
class Validator( Task ) :
    ''' a task that checks whether a previous task succeeded and records the result '''


################################
@export
class Daemon( Tool ) :
    '''keep repeating an action until killed'''

@export
class Service( Daemon ) :
    pass

@export
class Monitor( Daemon ) :
    pass


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
