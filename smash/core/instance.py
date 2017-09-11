#-- smash.core.instance

"""

"""

import logging

log = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################


from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from pathlib import Path

from ..util.meta import classproperty
from powertools import export
from .config import Config


#----------------------------------------------------------------------#

# this is where I can begin to flesh out the idea of config files being actual classes.

# todo: use cookiecutter to deploy an instance

@export
class InstanceTemplate :
    '''template specifying an instance structure'''

    def __init__( self, config: Config, filename: str, refname: str ) :
        self.config = config
        self.filename = filename
        self.refname = refname


#----------------------------------------------------------------------#

@export
class SmashTemplate( InstanceTemplate ) :
    ''''a default template for smash instance'''
    pass


#----------------------------------------------------------------------#

builtin_templates = {
    'smash' : SmashTemplate,
}

#----------------------------------------------------------------------#
