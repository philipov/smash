#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

__setup__ = dict(
    name            = 'smash',
    packages        = ['smash', 'smash.sys', 'smash.boot', 'smash.dash', 'smash.tools'],
    version         = '0.0.2',
    description     = __doc__,

    url             = 'https://github.com/philipov/smash',
    author          = 'Philip Loguinov',
    author_email    = 'philipov@gmail.com',

    entry_points    = {
        'console_scripts' : ['smash=smash:run'],
    },
    install_requires= [
        'psutil',
        'ruamel.yaml',
        'ordered_set',


        'click',
        'cookiecutter',
        'conda',
        'pytest',
        'colored_traceback',
        'colorama',
        'termcolor'
    ],
    classifiers     = [
        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Customer Service',

        'License :: Other/Proprietary License',

        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.6'
    ]
)

__version__ = __setup__['version']

__test_setup__= dict(

)


#----------------------------------------------------------------------#

from .cmdline import parse as parse_cmdline

from .__main__ import main
from .__main__ import enter

from .sys.config import Config
from .sys.config import ConfigTree

from .sys.export import Exporter
from .sys.export import ExportDebug
from .sys.export import ExportEnvironment

from .utils.out import debuglog
from .utils.out import loggers_for


#----------------------------------------------------------------------#

from .sys.plugins import plugins


#----------------------------------------------------------------------#

