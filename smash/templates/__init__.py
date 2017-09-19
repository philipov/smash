#-- smash.core.constants

"""
global constants
"""

from pathlib import Path

#----------------------------------------------------------------------#

TEMPLATES_ROOT          = Path( __file__ ).parents[0]

INSTANCE_CONFIG = TEMPLATES_ROOT / 'instance' / '__root__.yml'
ENV_CONFIG      = TEMPLATES_ROOT / 'instance' / '__env__.yml'
PKG_CONFIG      = TEMPLATES_ROOT / 'instance' / '__pkg__.yml'

PYTHON_CONFIG   = TEMPLATES_ROOT / 'python' / '__pkg__.yml'


#----------------------------------------------------------------------#
