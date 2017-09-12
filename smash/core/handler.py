#-- smash.core.handler

"""

"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

from pathlib import Path
from .config import Config
from .env import Environment

from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from ..util.meta import classproperty

from collections import OrderedDict

from powertools import export

#----------------------------------------------------------------------#

@export
class NoHandlerMatchedError(Exception):
    '''no handler picked up the file as a target it could provide the command string for'''

#----------------------------------------------------------------------#

@export
class Handler:
    ''' base class for setting up an action to be executed using a target file '''

    def __init__( self,
                  target:Path,
                  arguments,
                  env:Environment
                  ) -> None:
        self.target     = target
        self.arguments  = arguments
        self.env        = env

    def __run__( self, target: Path, arguments, env: Environment ):
        ''' this method is nominally static '''
        raise NotImplementedError()

    def run( self ) :
        ''' implement the __run__ magic method on subclasses '''
        #todo: this should return a future
        return self.__run__( self.target, self.arguments, self.env )


#----------------------------------------------------------------------#
@export
class MashHandler( Handler ) :
    '''this allows using the python interpreter defined by the virtual environment'''

    def __run__( self, target: Path, arguments, env: Environment ):
        '''read the file and do something with it'''
        raise NotImplementedError()


#----------------------------------------------------------------------#
@export
class CommandHandler( Handler ) :
    '''execute the target as-is'''

    def __run__( self, target:Path, arguments, env: Environment ) :
        env.run(target, *arguments)

@export
class Daemonizer( CommandHandler ):
    def __run__( self, target: Path, arguments, env: Environment ) :
        while True:
            task = super().__run__( Path(arguments[0]), arguments[1:], env )


#----------------------------------------------------------------------#
@export
class ScriptHandler( Handler ) :
    '''execute the script using its appropriate interpreter'''
    __interpreter__ = NotImplemented

    def __run__( self, target: Path, arguments, env: Environment ) :
        env.run( self.__interpreter__ + ' ' + str( target ), arguments )

@export
class BashHandler( ScriptHandler ) :
    '''this depends on a path to bash being defined in one of the config files. it could be the host, or a bash package'''
    __interpreter__ = 'bash'

@export
class BatchHandler( ScriptHandler ) :
    __interpreter__ = 'cmd'

@export
class PythonHandler( ScriptHandler ) :
    '''this allows using the python interpreter defined by the virtual environment'''
    __interpreter__ = 'python'


#----------------------------------------------------------------------#

### last in first out; use the first handler whose key regex matches the filename
builtin_handlers            = OrderedDict()

builtin_handlers['\.*']     = CommandHandler
builtin_handlers['start']   = Daemonizer

builtin_handlers['\.yml']   = MashHandler
builtin_handlers['\.yaml']  = MashHandler
builtin_handlers['\.msh']   = MashHandler

builtin_handlers['\.sh']    = BashHandler
builtin_handlers['\.bat']   = BatchHandler
builtin_handlers['\.py']    = PythonHandler


#----------------------------------------------------------------------#
