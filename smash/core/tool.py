#-- smash.core.tool

"""
isolate changes to the state of an environment so they can be tracked and versioned
"""


from powertools import AutoLogger
log = AutoLogger()
from powertools import term
from powertools import export
from powertools import assertion

from pathlib import Path
from .config import Config

from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from ..util.meta import classproperty
from .env import Environment

#----------------------------------------------------------------------#

from . import platform
Platform = platform.match()

@export
class Tool:
    ''' Base class for creating wrappers to keep track of state manipulation '''

    __slots__ = (
        'env',
        'config',
    )
    def __init__( self, env:Environment, config:Config) :
        self.env    = env
        self.config = config

    ### context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        pass

    ###
    def run(self):
        raise NotImplementedError




#----------------------------------------------------------------------#

@export
class Task( Tool ) :
    ''' perform an action once '''

    def run( self ) :
        return self.env.run( *self.command() )

    def command( self ) -> list:
        ''' call the command function for the appropriate platform'''
        cmd = list()
        if Platform == platform.Linux :
            cmd = self.command_linux()

        elif Platform == platform.Win32 :
            cmd = self.command_windows()

        elif Platform == platform.Mac :
            cmd = self.command_mac()

        with assertion( platform.PlatformError( self.command ) ) :
            assert len( cmd ) > 0

        return cmd


    ### abstract: platform-dependant implementations for self.command
    def command_windows( self ) -> list:
        raise NotImplementedError

    def command_linux( self ) -> list:
        raise NotImplementedError

    def command_mac( self ) -> list:
        raise NotImplementedError

#----------------------------------------------------------------------#



################################

@export
class Installer( Task ) :
    ''' install external dependencies using their own script '''

    class MissingSourceUrlError( Exception ) :
        '''source_url is NotImplemented'''

    source_url          = NotImplemented

    @property
    def download_destination( self ) -> Path :
        raise NotImplementedError

    @property
    def install_destination( self ) -> Path :
        raise NotImplementedError


    ################################
    filename_windows    = NotImplemented
    filename_linux      = NotImplemented
    filename_mac        = NotImplemented

    @property
    def installer_filename(self) -> str:
        # todo: further factor this platform-checking pattern
        filename = NotImplemented
        if Platform == platform.Linux :
            filename = self.filename_linux
        elif Platform == platform.Win32 :
            filename = self.filename_windows
        elif Platform == platform.Mac :
            filename = self.filename_mac

        with assertion( platform.PlatformError( 'unsupported platform' ) ) :
            assert filename is not NotImplemented

        return filename


    ################################
    def download( self) :
        ''' download the file for the appropriate platform from the source_url '''
        import wget

        with assertion( self.MissingSourceUrlError( type( self ) ) ) :
            assert self.source_url is not NotImplemented

        log.print(
            term.cyan(     'downloading: ' ),   term.dyellow( self.installer_filename),
            '\n',term.cyan('       from: '),    term.dyellow( self.source_url ),
            '\n',term.cyan('         to: '),    term.dyellow( self.download_destination ),
            '\n'
        )

        url             = self.source_url + self.installer_filename
        out_filepath    = wget.download( url, str(self.download_destination) )
        log.print( '' )


    ################################
    def install( self ) :
        log.print(
            term.cyan( '\n','running installer: ' ), term.dyellow( self.installer_filename ),
            ' in ', term.dyellow( self.download_destination ),
            '\n'
        )

        # block until install terminates
        proc = self.run()
        log.print(term.dyellow('Installing...'))
        next(proc)


#----------------------------------------------------------------------#

@export
class Loader( Task ) :
    ''' batch job for writing to a data store '''


@export
class Validator( Task ) :
    ''' a task that checks whether a previous task succeeded and records the result '''


class Lateralizer( Task ):
    ''' Spiral out. Keep going... '''


################################

@export
class Daemon( Tool ) :
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
    'Installer' : Installer,
    'Loader'    : Loader,
    'Validator' : Validator,

    'Daemon'    : Daemon,
    'Monitor'   : Monitor,
    'Service'   : Service,
}



#----------------------------------------------------------------------#
