#-- smash.set

'''

'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from powertools import term
from powertools.print import rprint, listprint, dictprint, pprint

from functools import partial
from contextlib import suppress
from ruamel.yaml.comments import CommentedMap
from copy import copy


from ..core.config import Config, ConfigTree
from ..core.config import getdeepitem

#----------------------------------------------------------------------------------------------#
__all__ = ['VALID_OPS'] # ...

OP_SET              = '='
OP_LIST_LEFT        = '['
OP_LIST_RIGHT       = ']'
TOKEN_SEP_FILE      = '::'
TOKEN_SEP_SECTION   = ':'
VALID_OPS           = (
    None,
    OP_SET,
    OP_LIST_LEFT,
    OP_LIST_RIGHT
)

##############################
@export
class NothingToDo(Exception):
    ''' no operator and value were specified, catch the early exit '''

# todo: input_value validation; should be pluggable

##############################
@export
def token_set( token:str, operator:str, input_value:str, configtree:ConfigTree ) -> Config:
    ''' perform a set operation on a config object
    '''

    ### parse token `configfile::`
    try:
        (configpath, rest) = token.split(TOKEN_SEP_FILE)
        print(configpath, rest)
        print(1)
    except ValueError as e:
        print(2)
        (configpath, rest) = configtree.env.filepath, token
    config:Config = configtree[configpath]

    ### parse token `section:section:key`
    keys = rest.split(TOKEN_SEP_SECTION)
    if len(keys) > 1:
        try:
            sections    = keys[:-1]
            key         = keys[-1]
        except IndexError as e:
            raise e
    elif len(keys) == 1:
        sections    = list()
        key         = keys[0]
    else:
        raise IndexError(token)

    ################################
    ### op: get and display value
    try:
        view = getdeepitem(config._yaml_data, sections)
    except KeyError as e:
        view = None #getdeepitem(config._yaml_data, copy(sections).pop())
    try:
        if key is '':
            key             = None
            current_value   = view
        elif isinstance(view, list):
            key = int(key)
            if key < 0:
                key = len(view) + key
            current_value = view[key]
        else:
            current_value = view[key]
    except KeyError as e:
        current_value = None

    log.print(
        "\n", term.green('SHOW: '),
       configpath, TOKEN_SEP_FILE,
       sections, TOKEN_SEP_SECTION,
       key, term.green(f' {OP_SET} '), current_value
    )

    ################################
    if operator is input_value is None:
        raise NothingToDo(config)

    ################################
    ### else: apply operator
    new_value = NotImplemented

    int_value, float_value = (None, None)   ### infer <value> type: int > float > str|None
    with suppress(TypeError, ValueError):   int_value   = int( input_value )
    with suppress(TypeError, ValueError):   float_value = float( input_value )

    if   int_value is not None:             input_value = int_value
    elif float_value is not None:           input_value = float_value

    ###     SET/DELETE SCALAR VALUE
    if operator == OP_SET:

        ### [null input]
        if input_value is None:

            ### todo: op: delete section -- s1:s2: = None
            if key is None:
                raise NotImplementedError('todo: delete section')

            ### op: delete item -- s1:s2:k = None
            else:
                del view[key]
                new_value = None

        ### [given input]
        else:

            ### todo: op: assign container to section -- s1:s2:s3: = seq|map
            if key is None:
                if   input_value.lower() in ('seq', 'list'):  view = list()
                elif input_value.lower() in ('map', 'dict'):  view = CommentedMap()
                else:
                    raise ValueError("value must be 'map' or 'seq' when assigning to a section")
                if len(sections) == 1:
                    config._yaml_data[sections[0]] = view
                else:
                    outer       = copy(sections)
                    section     = outer.pop()
                    getdeepitem(config._yaml_data, outer)[section] \
                                = view
                new_value = view
                rprint(config._yaml_data)

            ### op: assign item to key -- s1:s2:k = str|int|float
            else:
                view[key]:str   = input_value
                new_value       = view[key]

    ################################
    ###     LIST OPERATIONS
    elif operator in (OP_LIST_LEFT, OP_LIST_RIGHT):

        ### [null input]
        if input_value is None \
        and isinstance(view, (list, CommentedMap)):

            ### op: pop the left or right of list -- s1:s2: [ None
            if key is None:
                {   OP_LIST_LEFT:   partial(view.pop,  0),
                    OP_LIST_RIGHT:  view.pop,
                }[operator]()
                new_value = None

            ### op: move key's position left or right in its container -- s1:s2:k [ None
            else:
                if isinstance(view, CommentedMap): ### mappings have different key structure from sequences
                    def convert(k):
                        i = list( view.items() ).index( (k, view[k]) )
                        if i < 0:
                            i = len(view) - i
                        return i
                else:
                    convert = int

                ### calculate new position
                if   operator == OP_LIST_LEFT:
                    if convert(key) == 0:           new = len(view)
                    else:                           new = convert(key)-1
                elif operator == OP_LIST_RIGHT:
                    if convert(key) == len(view)-1: new = 0
                    else:                           new = convert(key)+1

                ###
                if isinstance(view,CommentedMap): ### which requires a different execution
                    log.info(f'new:{new} key:{key} = {current_value}')
                    del view[key]
                    view.insert(new, key, current_value)
                    new_value = view[key]
                else:
                    view.pop(key)
                    view.insert(new, current_value)
                    new_value = view[new-1]

        ### [given input]

        elif isinstance(current_value, list):                   ### token points to list

            ### op: append <value> to left or right of end of a list -- s1:s2: [ str|int|float
            if key is None:
                {   OP_LIST_LEFT:   partial(view.insert,  0),
                    OP_LIST_RIGHT:  view.append,
                }[operator]( input_value )

                outer       = copy(sections)
                section     = outer.pop()
                new_value   = getdeepitem(config._yaml_data, outer)[section]


            ### todo: op: move key's position left or right by <value:int> indices -- s1:s2:k [ int
            else:
                {   OP_LIST_LEFT:   partial(current_value.insert, 0),
                    OP_LIST_RIGHT:  current_value.append,
                }[operator]( input_value )
                raise NotImplementedError('todo: move item V spaces')
                new_value = view[key]

        elif isinstance(current_value, (str, int, float)) \
        and isinstance(view, list):                             # token points to scalar, in a list

            ### op: insert <value> next to <key> in a list -- s1:s2: [ str|int|float
            if key is None:
                {   OP_LIST_LEFT:   partial(view.insert,  0),
                    OP_LIST_RIGHT:  view.append,
                }[operator]( input_value )


            ### op: insert <value> next to <key> in a list -- s1:s2:k [ str|int|float
            else:
                {   OP_LIST_LEFT:   partial(view.insert, key),
                    OP_LIST_RIGHT:  partial(view.insert, key+1),
                }[operator]( input_value )

        ### [exception]
        else:
            raise TypeError(f'invalid type (view={type(view)}, current_value={type(current_value)}) for sequence setters')


    ################################
    log.print(
        "\n", term.green('SET:  '),
        configpath, TOKEN_SEP_FILE,
        sections, TOKEN_SEP_SECTION,
        key, term.green(f' {OP_SET} '), new_value
    )

    return config


##############################

#----------------------------------------------------------------------------------------------#
