#-- smash.constants

"""
global constants
"""

__setup__ = dict(
    name='smash',
    packages=['smash', 'smash.sys', 'smash.boot', 'smash.dash', 'smash.tools'],
    version='0.0.2',
    description=__doc__,

    url='https://github.com/philipov/smash',
    author='Philip Loguinov',
    author_email='philipov@gmail.com',

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
        'pytest',
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

__version__ = __setup__['version']

__test_setup__ = dict(
    install_requires=[
        'pytest'
    ]
)

__dev_setup__ = dict(
    install_requires=[
        'pytest'
    ]
)

#----------------------------------------------------------------------#

config_protocol = 0


#----------------------------------------------------------------------#
