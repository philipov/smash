#-- smash.set

'''

'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from powertools import term

from functools import partial
from contextlib import suppress
from ruamel.yaml.comments import CommentedMap


from ..core.config import Config, ConfigTree
from ..core.config import getdeepitem

#----------------------------------------------------------------------------------------------#
__all__ = ['VALID_OPS']

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
        the config object to use is either the environment config,
            or specified in the token using ::
        if a value is specified
            `=` will assign a scalar to a key
            `=` will create a new section, value can be 'list' or 'map'
            `[` and `]` on a key inserts the value next to the key, if section is a list
            `[` or `]` on a section append the value to the section, if section is a list
        if there is no value to set:
            `=` will delete a key
            `[` and `]` on a key move it up or down in its container
            `[` or `]` on a section pop a value, if section is a list
    '''

    ### parse token `configfile::`
    try:
        (configpath, rest) = token.split(TOKEN_SEP_FILE)[0]
    except ValueError as e:
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

    ### op: display value
    try:
        view = getdeepitem(config._yaml_data, sections)
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
        raise e
    log.print( "\n", term.green('SHOW: '), configpath, TOKEN_SEP_FILE, sections, TOKEN_SEP_SECTION, key, term.green(f' {OP_SET} '), current_value )


    if operator is input_value is None:
        raise NothingToDo(config)

    ### else: apply operator
    new_value= NotImplemented

    int_value, float_value = (None, None)   ### infer <value> type: int > float > str
    with suppress(TypeError, ValueError):
        int_value = int( input_value )
    with suppress(TypeError, ValueError):
        float_value = float( input_value )

    if int_value is not None:       # int
        input_value = int_value
    elif float_value is not None:   # float
        input_value = float_value

    ###     SET/DELETE SCALAR VALUE
    if operator == OP_SET:
        ### op: delete item -- s1:s2:k = None
        if input_value is None:
            del view[key]
            new_value = None
            if key is None:
                    pass

        else:
            ### op: assign container to section -- s1:s2:s3: = seq|map
            if key is None:
                pass

            ### op: assign item to key -- s1:s2:k = str|int|float
            else:
                view[key]:str = input_value
                new_value = view[key]

    ###     LIST OPERATIONS
    elif operator in (OP_LIST_LEFT, OP_LIST_RIGHT):

        ### null input:
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
                if isinstance(view, CommentedMap): ### mappings have different key structure
                    def convert(k):
                        i = list( view.items() ).index( (k, view[k]) )
                        if i < 0:
                            i = len(view) - i
                        return i
                else:
                    convert = int

                ### calculate new position
                if operator == OP_LIST_LEFT:
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

        ### given input:

        elif isinstance(current_value, list):                   ### token points to list
            ### op: append <value> to left or right of end of a list -- s1:s2: [ val
            if key is None:
                {   OP_LIST_LEFT:   partial(view.insert,  0),
                    OP_LIST_RIGHT:  view.append,
                }[operator]( input_value)
            ### todo: op: move key's position left or right by <value:int> indices -- s1:s2:k [ int
            else:
                {   OP_LIST_LEFT:   partial(current_value.insert, 0),
                    OP_LIST_RIGHT:  current_value.append,
                }[operator]( input_value )
                raise NotImplementedError('todo: move item V spaces')
                new_value = view[key]

        elif isinstance(current_value, (str, int, float)) \
        and isinstance(view, list):                             # token points to scalar
            ### op: insert <value> next to <key> in a list -- s1:s2: [ val
            if key is None:
                {   OP_LIST_LEFT:   partial(view.insert, key),
                    OP_LIST_RIGHT:  partial(view.insert, key+1),
                }[operator]( input_value )
            ### op: insert <value> next to <key> in a list -- s1:s2:k [ val
            else:
                {   OP_LIST_LEFT:   partial(view.insert, key),
                    OP_LIST_RIGHT:  partial(view.insert, key+1),
                }[operator]( input_value )

        else:
            raise TypeError(f'invalid type ({type(view)}, {type(current_value)}) for list setters')


    log.print(
        "\n", term.green('SET:  '),
        configpath, TOKEN_SEP_FILE,
        sections, TOKEN_SEP_SECTION,
        key, term.green(f' {OP_SET} '), new_value
    )

    return config


##############################

#----------------------------------------------------------------------------------------------#
