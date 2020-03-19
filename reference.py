from batteries import *
from common import *
import ijson
import collections
import copy
import prettytable
'''
    Problems:
        smaller number of results for data_type (for booltest - only data_type no exid, batteries)
        incorrect item - non existing CFG, test name, data_type
        bad results of test
            - remove test
            - filter bad results only
        
        problems =  set(serialize(atts)) 
'''


# def count_results(data, filename = '', num_items = 10000 ):
#     '''Expected count of results for given size'''
#     hist = collections.Counter(map(lambda item: serialize(item, ['size', 'data_type']), data))
#
#     tree = {}
#     for key, freq in hist.items():
#         keys = size, data_type = key.split('&')
#         add_value(tree, keys, freq, dict)
#     if filename:
#         save_json_file(tree, filename=filename)
#     return {size: max(tree[size].values())for size in tree }
# def filter_reference(failed_unitests):
#     problematic = {}
#     OK = {}
#     for unitest, freqs in failed_unitests.items():
#         if '1e-08' in freqs or freqs['10'] < 10:
#             problematic[unitest] = freqs
#         else:
#             OK[unitest] = freqs
#
#     save_json_file(OK, 'Random_data/unitest_num_failed_OK.json')
#     save_json_file(problematic, 'Random_data/unitest_num_failed_BAD.json')


# def extract_small_pvals(json_items):
#     bound = 10 ** -9
#     res = []
#     count = 0
#     for item_dic in json_items:
#         # if item_dic['seed'] == '0000000000000470' and item_dic['subtest'] == "sub: var:800|1000000 idx:148":
#         #     print(item_dic)
#         #     return
#         if item_dic['p-val'] < bound:
#             item_dic['p-val'] = str(item_dic['p-val'])
#             res.append(copy.deepcopy(item_dic))
#
#             # count += 1
#             # if count == 100:
#             #     break
#     save_json_file(res, 'Random_data/items_below_1e-09.json')
def skip_problematic_gen(data, problematic_keys, atts):
    def is_problematic(item_dic, atts, problematic_keys):
        for att in atts:
            key = serialize(item_dict, att)
            if key in problematic_keys:
                return True
        return False
    for item_dict in data:
        if is_problematic(item_dict, atts, problematic_keys):
            continue
        yield item_dict
def compute_AES_stats(problematic_keys, atts):
    item_gen = stream_item_gen(file_name='rtt-results-dump-43-44-46-48-51-52-54.json', gen = batteries_dump_gen)
    hist = collections.defaultdict(lambda : collections.defaultdict(lambda :0))
    count = 0
    alphas = {10**(-e):0 for e in [-1] + list(range(2,12))}
    for item_dic in skip_problematic_gen(item_gen, problematic_keys, atts):
        key =  serialize(item_dic, ['size'] + TEST_KEYS)
        for alpha in alphas:
            if item_dic['p-val'] < alpha:
                hist[key][alpha] += 1
        # count += 1
        # if count == 1000:
        #     break

    return hist
def stream_item_gen(file_name, gen = batteries_dump_gen, path='/mnt/c/sysox/DATA/'):
    '''Large file generator'''
    json_file = open(path+file_name)
    json_items = ijson.items(json_file, 'item')
    item_gen = gen(json_items)
    return item_gen
def problematic(gen = batteries_dump_gen, expected_counts = {'10MiB':419, '100MiB':456}):
    #   compute problematic data_type (experiment setting) based on smaller nubmer of results, very small p-values (10^-8) and bad test name
    #
    tests = load_json_file('Cryptostreams_data/tests.json')
    problematic_data_types = set()
    bound = 10**-8
    item_gen = stream_item_gen(file_name='rtt-results-dump-43-44-46-48-51-52-54.json', gen = batteries_dump_gen)

    hist = collections.defaultdict(lambda :collections.defaultdict(lambda : 0))

    #bad test names + below bound + computation of data_type histograms
    for item_dict in item_gen:
        size = item_dict['size']
        data_type = item_dict['data_type']
        hist[size][data_type] += 1
        unitests = serialize(item_dict, TEST_KEYS)
        if  unitests not in tests[size]['unitest']:
            problematic_data_types.add(item_dict['data_type'])
        if item_dict['p-val'] < bound:
            problematic_data_types.add(item_dict['data_type'])

    # bad counts
    for size in hist:
        expected_freq = expected_counts[size]
        for data_type, freq in hist[size].items():
            if freq != expected_freq:
                problematic_data_types.add(data_type)
    save_json_file(problematic_data_types, '/Random_data/problematic_datatypes_final_1e-08.json')
    return problematic_data_types
def reference_overview(atts, dst_filename = '/Random_data/items_below_1e-09_overview.json', max_lvl=-1):
    small_pvals = load_json_file('Random_data/items_below_1e-09.json')
    tree = {}
    # counter = 0
    for item_dic in small_pvals:
        # if counter == 10000:
        #     break
        # counter += 1
        keys = [serialize(item_dic, att) for att in atts]
        value = item_dic['p-val']
        add_value(tree, keys, value, list)
    counts_nodes(tree)
    print_tree(tree, key = None, lvl = 0, file_name=dst_filename,  max_lvl= max_lvl)
def create_row_table(header, rows):
    table = prettytable.PrettyTable(header)
    for row in rows:
        if len(row) < len(header):
            table.add_row(row + [0]*(len(header)-len(row)))
        else:
            table.add_row(row)
    return table
def compute_freqs(file_name = '', path='/mnt/c/sysox/DATA/' ):
    if file_name:
        sys.stdout = open(path + file_name, 'w')

    stats = load_json_file('Random_data/final_stats.json')
    tests = load_json_file('Cryptostreams_data/tests.json')

    res = collections.defaultdict(lambda: collections.defaultdict(lambda :collections.defaultdict(collections.Counter)))
    cumulative_hist = collections.Counter()
    for unitest, hist in stats.items():
        cumulative_hist.update(hist)
        size_and_unitest = unitest.split('&')
        size, test_items = size_and_unitest[0], size_and_unitest[1:]
        for idx, test_lvl in enumerate(TEST_KEYS):
            test_name = '&'.join(test_items[:idx+1])
            res[size][test_lvl][test_name].update(hist)

    for size in res:
        for test_lvl in res[size]:
            header = [size + ' ' + test_lvl] + list(cumulative_hist.keys())
            rows = [ [test_name] + list(res[size][test_lvl][test_name].values()) for test_name in res[size][test_lvl] ]
            # print(len(header), len(rows[0]))
            table = create_row_table(header, rows)
            print(table)
            print('\n\n\n')

    if file_name:
        sys.stdou = sys.__stdout__

#                                                            Overview of raw results
# reference_overview(['size', 'exid'], '/Random_data/below_1e-09_pvals_exid.json')
# reference_overview(['size', 'test'], '/Random_data/below_1e-09_pvals_test.json')
# reference_overview(['size', 'test', 'exid'], '/Random_data/below_1e-09_pvals_exid_test.json')

#                                                            Eliminate bad names of tests and smaller number of results for
# problematic_datatypes = problematic()
# problematic_datatypes = load_json_file('Random_data/problematic_datatypes_final_1e-08.json')
# stats = compute_AES_stats(set(problematic_datatypes), ['data_type'])



#                                                           FINAL OUTPUT

#                                                           clear data
# problematic_datatypes = load_json_file('Random_data/problematic_datatypes_1e-08.json')
# problematic_datatypes.append('TestU01 Rabbit&smultin_MultinomialBitsOver')
# save_json_file(problematic_datatypes, 'Random_data/final_problematic_items.json')
problematic_items_final = load_json_file('Random_data/final_problematic_items.json')
final_stats = compute_AES_stats(set(problematic_items_final), ['data_type', ['battery','test']])
save_json_file(final_stats, 'Random_data/final_stats.json')
# compute_freqs('Random_data/Table_stats_final.txt')
#                                                           Create artefacts




