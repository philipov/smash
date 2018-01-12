#-- smash.setup.arguments

'''--- Smart Shell
    An integrated environment for reproducible research, development, testing, and production
'''

from pathlib import Path
import os

#----------------------------------------------------------------------------------------------#

def collect_package_data( package_path ) :
    root_path = Path( __file__ ).parents[2].resolve() / package_path
    package_data = list()

    for root, _, _ in os.walk( str( root_path ) ) :
        package_data.append( str( Path( root ) / '*' ) )

    return package_data


#----------------------------------------------------------------------------------------------#

kwargs = dict(
    name            = 'smash',
    version         = '0.0.4',
    description     = __doc__,
    license         = "MIT License",

    url             = 'https://github.com/philipov/smash',
    author          = 'Philip Loguinov',
    author_email    = 'philipov@gmail.com',

    packages = [
        'smash',            # main application

        'smash.core',       # fundamental abstractions
        'smash.tool',       # extensive subapplications
        'smash.util',       # low-level utilities
        'smash.test',       # testing plugins and utilities
        'smash.templates',  # library of default files

        'smash.bang',       # instance and box management cli
        'smash.dash',       # graphical admin and monitoring interface

    ],

    zip_safe                = True,
    include_package_data    = True,
    package_data = {
        'smash.templates' : collect_package_data( Path('smash')/'templates' )
    },
    entry_points = {
        'console_scripts': [
            'smash      = smash:console',

            'smash.bang = smash.bang:console',
            'smash!     = smash.bang:console',

            'smash.dash = smash.dash:console',
            'smash-     = smash.dash:console',
        ],
    },
    install_requires = [
        'powertools',       # std lib extension
        'psutil',           # process utils
        'ruamel.yaml',      # yaml parser
        'xmltodict',        # xml parser
        'python-box',       # attribute-addressable nested dictionaries
        'treelib',          # data structure
        'ordered_set',      # data structure


        'click',            # command-line parser
        'cookiecutter',     # filesystem templater
        'conda',            # package manager
        'dulwich',          # git
        'wget',             # downloader

        'colored_traceback',# depr.
        'colorama',
        'termcolor',
    ],
    classifiers = [
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

from copy import deepcopy
test_kwargs = deepcopy( kwargs )
test_kwargs['install_requires'].append( 'pytest' )

dev_kwargs = deepcopy( test_kwargs )

__version__ = kwargs['version']

#----------------------------------------------------------------------------------------------#
