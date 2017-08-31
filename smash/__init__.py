#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

__setup__ = dict(
    name            = 'smash',
    packages        = ['smash', 'smash.sys', 'smash.ext'],
    version         = '0.0.2',
    description     = __doc__,

    url             = 'https://github.com/philipov/smash',
    author          = 'Philip Loguinov',
    author_email    = 'philipov@gmail.com',

    entry_points    = {
        'console_scripts' : ['smash=smash:run'],
    },
    requires        = [
        'psutil',
        'ruamel.yaml',
        'ordered_set',

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
from .__main__ import run

from .sys.config import Config
from .sys.config import ConfigTree


#----------------------------------------------------------------------#
