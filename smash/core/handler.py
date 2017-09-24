#-- smash.core.handler

"""

"""


from powertools import AutoLogger
log = AutoLogger()

################################

from pathlib import Path
from .config import Config
from .env import Environment

from powertools import term
from powertools.print import rprint
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
                  arguments:list,
                  env:Environment
                  ) -> None:
        self.target     = target
        self.arguments  = arguments
        self.env        = env

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ):
        ''' this method is nominally static '''
        raise NotImplementedError()

    def run( self, ctx ) :
        ''' implement the __run__ magic method on subclasses '''
        #todo: this should return a future
        return self.__run__( self.target, self.arguments, self.env, ctx=ctx )


#----------------------------------------------------------------------#
@export
class MashHandler( Handler ) :
    '''this allows using the python interpreter defined by the virtual environment'''

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ):
        '''read the file and do something with it'''
        raise NotImplementedError()


def make_ClickHandler(func):
    class ClickHandler( Handler ):
        def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
            log.print(term.red(command, arguments))
            ctx.invoke( func, *arguments )
    return ClickHandler

#----------------------------------------------------------------------#
@export
class SubprocessHandler( Handler ) :
    '''execute the target as-is'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        env.run(command, *arguments)

@export
class Daemonizer( SubprocessHandler ):
    def __run__( self, command, arguments:list, env: Environment, *, ctx=None ) :
        while True:
            print('subcommand', arguments)
            subcommand = Path( arguments[0] )
            subarguments = arguments[1:2]
            task = super().__run__( subcommand, subarguments, env )

@export
class ToolHandler( Handler ) :
    '''command is a tool invocation'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        env.run( command, *arguments )

@export
class MouthHandler( Handler ) :
    '''print fortune'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        env.run( command, *arguments )

#----------------------------------------------------------------------#
@export
class ScriptHandler( Handler ) :
    '''execute the script using its appropriate interpreter'''
    __interpreter__ = NotImplemented

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ) :
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

from .. import pkg

### last in first term; use the first handler whose key regex matches the filename
builtin_handlers            = OrderedDict()
builtin_handlers['\.*']     = SubprocessHandler # default

#todo: can these subcommands be integrated with click?
builtin_handlers['begin']   = Daemonizer
builtin_handlers['with']    = ToolHandler
builtin_handlers['mouth']   = MouthHandler


builtin_handlers['\.yml']   = MashHandler
builtin_handlers['\.yaml']  = MashHandler
builtin_handlers['\.msh']   = MashHandler

builtin_handlers['\.sh']    = BashHandler
builtin_handlers['\.bat']   = BatchHandler
builtin_handlers['\.py']    = PythonHandler


#----------------------------------------------------------------------#
