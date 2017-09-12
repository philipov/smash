#-- smash.setup.arguments

'''
store setup parameters inside namespace subpackage to avoid importing the library during setup.
'''

#----------------------------------------------------------------------#

kwargs = dict(
    name        = 'smash',
    packages    = [
        'smash',
        'smash.setup',
        'smash.core',
        'smash.boot',
        'smash.dash',
        'smash.tool',
        'smash.util'
    ],
    version     = '0.0.2',
    description = __doc__,

    url         = 'https://github.com/philipov/smash',
    author      = 'Philip Loguinov',
    author_email= 'philipov@gmail.com',

    entry_points={
        'console_scripts' : ['smash=smash:console'],
    },
    install_requires=[
        'psutil',
        'ruamel.yaml',
        'ordered_set',

        'click',
        'cookiecutter',
        'conda',

        'colored_traceback',
        'colorama',
        'termcolor'
    ],
    classifiers=[
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

#----------------------------------------------------------------------#
