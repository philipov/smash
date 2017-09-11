#-- smash.cmdline

"""
parse command-line arguments
"""


import argparse

from collections import namedtuple

import logging

log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print
# log.debug = lambda *a, **b : None

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try:
        __all__.append(obj.__name__)
    except AttributeError:
        __all__.append(obj.__main__.__name__)
    return obj

#----------------------------------------------------------------------#

_argnames   = list()
_parser     = argparse.ArgumentParser(
    description="Smart Shell"
)

def _add_argument(name, options=(), **kwargs):
    print('add argument', name, options, kwargs)
    _parser.add_argument(*options, dest=name, **kwargs)
    _argnames.append(name)


#################### main
_add_argument('mode',
    type    = str,
    help    = 'execution mode',
)

_add_argument('target',
    type    = str,
    nargs   = argparse.REMAINDER,
    help    = 'what is to be executed',
)

#################### flags

_add_argument('verbose',
    options = ('-v', '--verbose'),
    action  = 'store_true',
    help    = 'print extra information'
)

####################
Arguments = namedtuple('Arguments', _argnames)
export(Arguments)


####################
@export
def parse( argv: list = None ) -> Arguments :
    args = _parser.parse_args( argv )
    return Arguments( **args.__dict__ )


#----------------------------------------------------------------------#
