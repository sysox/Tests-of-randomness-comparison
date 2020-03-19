import collections
import json
import my_tree
import decimal
def print_json(data):
    json.dumps(data, indent=4)

#                                                   FILE manipulation
def containers_customize(obj):
    """sorted lists, sets to lists"""
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    if isinstance(obj, collections.Mapping):
        return {key: containers_customize(obj[key]) for key in obj}
    if isinstance(obj, list) or isinstance(obj, set):
        obj = list(obj)
        try:
            return sorted(obj)
        except:
            return [containers_customize(item) for item in obj]
    return obj
class CustomJsonEncoder(json.JSONEncoder):
    def encode(self, obj):
        return super(CustomJsonEncoder, self).encode(containers_customize(obj))
def load_json_file(file_name, path='/mnt/c/sysox/DATA/'):
    """Load json """
    with open(path+file_name) as json_file:
        data = json.load(json_file)
        return data
def save_json_file(data, file_name, path='/mnt/c/sysox/DATA/'):
    with open(path + file_name, 'w') as f:
        json.dump(containers_customize(data), f, indent=4, cls=CustomJsonEncoder)


#                                                   Constants
TEST_KEYS = ['battery', 'test', 'subtest', 'unitest']
FUNC_KEYS = ['size', 'strategy', 'func', 'round']
CONF_KEYS = TEST_KEYS + FUNC_KEYS
SEED_KEYS = ['seed', 'offset', 'byte']
RESULT_KEYS = ['stats']
#                                                   DICT manipulation
def serialize(dict_, keys):
    """returns string of values separated by &"""
    """"""
    res = ''

    #only one key
    if not isinstance(keys, collections.abc.Iterable) or isinstance(keys, str):
        return dict_[keys]

    for key in keys:
        if key not in dict_:
            to_append = '-'
        else:
            to_append = str(dict_[key])
        if res == '':
            res = to_append
        else:
            res += '&' + to_append

    return res
#map(upper, mylis)
#                                                   Parsing, file reading
def add_values(fields, keys, dict_):
    """for all keys: add key:value (value is just behind the key in field list)"""
    for key in keys:
        try:
            ind = fields.index(key)
            dict_[key] = fields[ind + 1]
        except ValueError:
            pass
def parse_data_type(data_type):
    res = {}
    fields = data_type.split('_')
    add_values(fields, ['key', 'off', 'seed', 'der'], res)
    res['RUN'] = fields[0][14:]
    if fields[1] in ['ctr', 'hw', 'sac']:
        res['strategy'] = fields[1]
    for field in fields:
        if ('MiB' in field) or ('MiB' in field):
            res['size'] = field
    res['func'] = fields[-3]
    res['round'] = fields[-2][1:]
    res['block_size'] = fields[-1][1:-4]
    return res




