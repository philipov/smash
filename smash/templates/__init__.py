#-- smash.core.constants

"""
global constants
"""

from pathlib import Path

#----------------------------------------------------------------------------------------------#

##########################################################
ROOT_YAMLispNode        = '__root__.yml'
ENV_YAMLispNode         = '__env__.yml'
PKG_YAMLispNode         = '__pkg__.yml'
BOX_YAMLispNode         = '__box__.yml'

WIN_YAMLispNode         = '__win__.yml'
NIX_YAMLispNode         = '__nix__.yml'
MAC_YAMLispNode         = '__mac__.yml'

GITIGNORE           = '.gitignore'
README              = 'README.md'


##########################################################
TEMPLATES_ROOT      = Path( __file__ ).parents[0] # this file's directory at time of import.

STOP_FILE           = TEMPLATES_ROOT / '__stop__'
SMASH_PY            = TEMPLATES_ROOT / 'smash.py'
SMASH_SPEC          = TEMPLATES_ROOT / 'smash.spec'

INSTANCE_BLANK      = TEMPLATES_ROOT / ROOT_YAMLispNode
ENV_BLANK           = TEMPLATES_ROOT / ENV_YAMLispNode
PKG_BLANK           = TEMPLATES_ROOT / PKG_YAMLispNode
BOX_BLANK           = TEMPLATES_ROOT / BOX_YAMLispNode

GITIGNORE_BLANK     = TEMPLATES_ROOT / GITIGNORE
README_BLANK        = TEMPLATES_ROOT / README

HOST                = TEMPLATES_ROOT / 'host'
NET                 = TEMPLATES_ROOT / 'net'
PLATFORM            = TEMPLATES_ROOT / 'platform'

PYTHON              = TEMPLATES_ROOT / 'python'


##########################################################

#----------------------------------------------------------------------------------------------#

##########################################################
PARENTS_SECTION     = '__inherit__'
EXPORT_SECTION      = '__export__'
SCRIPT_SECTION      = '__script__'


##########################################################
BOX_SECTION         = 'box'


##########################################################
SHELL_VARS_SECTION  = 'var'


##########################################################
PATH_VARS_SECTION   = 'path'

PATH_ROOT           = 'ROOT'
PATH_BOXES          = 'BOXES'


##########################################################

#----------------------------------------------------------------------------------------------#
