#-- smash.set

'''

'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from powertools import term

from functools import partial
from ruamel.yaml.comments import CommentedMap


from ..core.config import Config, ConfigTree
from ..core.config import getdeepitem

#----------------------------------------------------------------------#
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


##############################
@export
def token_set( token:str, operator:str, value:str, configtree:ConfigTree ) -> Config:
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

    ## configfile::
    try:
        (configpath, rest) = token.split(TOKEN_SEP_FILE)[0]
    except ValueError as e:
        (configpath, rest) = configtree.env.filepath, token
    config:Config = configtree[configpath]

    # ### section:section:key
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

    ### display value
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

    ### early exit
    if operator is value is None:
        raise NothingToDo(config)

    ### apply operator
    new_value = NotImplemented

    try:
        value = int(value)
    except TypeError as e:
        pass
    except ValueError as e:
        pass

    ###     SET SCALAR VALUE
    if operator == OP_SET:
        ### delete item
        if value is None:
            del view[key]
            new_value = None

        ### assign item
        else:
            view[key]:str = value
            new_value = view[key]

    ###     LIST OPERATIONS
    elif operator in (OP_LIST_LEFT, OP_LIST_RIGHT):

        if value is None \
        and isinstance(view, (list, CommentedMap)): ### null-op on sequence

            ### pop the left or right of list
            if key is None:
                {   OP_LIST_LEFT:   partial(view.pop,  0),
                    OP_LIST_RIGHT:  view.pop,
                }[operator]()
                new_value = None

            ### move key up or down in order
            else:
                if isinstance(view, CommentedMap):
                    def convert(k):
                        i = list( view.items() ).index( (k, view[k]) )
                        if i < 0:
                            i = len(view) - i
                        return i
                else:
                    convert = int

                if operator == OP_LIST_LEFT:
                    if convert(key) == 0:
                        new = len(view)
                    else:
                        new = convert(key)-1
                elif operator == OP_LIST_RIGHT:
                    if convert(key) == len(view)-1:
                        new = 0
                    else:
                        new = convert(key)+1
                else:
                    raise RuntimeError('move left or right')

                if isinstance(view,CommentedMap):
                    log.info(f'new:{new} key:{key} = {current_value}')
                    del view[key]
                    view.insert(new, key, current_value)
                    new_value = view[key]
                else:
                    view.pop(key)
                    view.insert(new, current_value)
                    new_value = view[new-1]

        # todo: finish operator consistency, then document
        ### append to left or right of list
        elif isinstance(current_value, list):
            {   OP_LIST_LEFT:   partial(current_value.insert, 0),
                OP_LIST_RIGHT:  current_value.append,
            }[operator](value)
            new_value = view[key]

        ### insert value next to key
        elif isinstance(current_value, str) \
        and isinstance(view, list):
            {   OP_LIST_LEFT:   partial(view.insert, key),
                OP_LIST_RIGHT:  partial(view.insert, key+1),
            }[operator](value)
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

#----------------------------------------------------------------------#
