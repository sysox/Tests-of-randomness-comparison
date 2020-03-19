from booltest import *
from batteries import *
from common import *

def get_tests(data, generator, overview_file_path, dst_file_path, short = False):
    # cryptostreams_data = load_json_file('small_rtt-results-dump-25-26-27.json')
    tree = {}
    for item_dict in generator(data):
        for idx, test_lvl in enumerate(TEST_KEYS):
            if not short:
                keys = [item_dict['size'], TEST_KEYS[idx]]
                value = serialize(item_dict, TEST_KEYS[:idx+1])
            else:
                keys =  [item_dict[key] for key in  TEST_KEYS]
                value = serialize(item_dict, TEST_KEYS)
            add_value(tree, keys, value, set)
    save_json_file(tree, dst_file_path)
    counts_nodes(tree)
    print_tree(tree, key = None, lvl = 0, file_name = overview_file_path)
def get_PRNG(data, generator, overview_file_path, dst_file_path, short = False):
    tree = {}
    for item_dict in generator(data):
        for idx, test_lvl in enumerate(FUNC_KEYS):
            if not short:
                keys = [item_dict['size'], FUNC_KEYS[idx]]
                value = serialize(item_dict, FUNC_KEYS[:idx+1])
            else:
                keys =  [item_dict[key] for key in  FUNC_KEYS]
                value = serialize(item_dict, FUNC_KEYS)

            add_value(tree, keys, value, set)
    save_json_file(tree, dst_file_path)
    counts_nodes(tree)
    print_tree(tree, key = None, lvl = 0, file_name=overview_file_path)




#                                                   BATTERIES
cryptostreams_data = load_json_file('rtt-results-dump-25-26-27.json')
#                                                   get tests
get_tests( cryptostreams_data,  batteries_dump_gen, \
           overview_file_path='Cryptostreams_data/tests_overview.txt',  \
           dst_file_path='Cryptostreams_data/tests.json', \
           short = False)
get_tests( cryptostreams_data,  batteries_dump_gen, \
           overview_file_path='Cryptostreams_data/tests_overview_short.txt', \
           dst_file_path='Cryptostreams_data/tests_short.json', \
           short = True)
#                                                   get CFG
get_PRNG( cryptostreams_data,  batteries_dump_gen, \
           overview_file_path='Cryptostreams_data/CFGs_overview.txt' \
           , dst_file_path='Cryptostreams_data/CFGs.json', \
           short = False)
get_PRNG( cryptostreams_data,  batteries_dump_gen, \
           overview_file_path='Cryptostreams_data/CFGs_overview_short.txt', \
           dst_file_path='Cryptostreams_data/CFGs_short.json', \
           short = True)


#                                                   BOOLTEST

cryptostreams_data = load_json_file('booltest-results-dump-25-26-27.json')
#                                                   get tests
get_tests( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest_tests_overview.txt', \
           dst_file_path='Cryptostreams_data/booltest_tests.json', \
           short = False)
get_tests( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest_tests_overview_short.txt', \
           dst_file_path='Cryptostreams_data/booltest_tests_short.json', \
           short = True)
#                                                   get CFG
get_PRNG( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest_CFGs_overview.txt', \
           dst_file_path='Cryptostreams_data/booltest_CFGs.json', \
           short = False)
get_PRNG( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest_CFGs_overview_short.txt', \
           dst_file_path='Cryptostreams_data/booltest_CFGs_short.json', \
           short = True)

#                                                   BOOLTEST v2

cryptostreams_data = load_json_file('booltest2-results-dump-25-26-27.json')
#                                                   get tests
get_tests( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest2_tests_overviewtxt', \
           dst_file_path='Cryptostreams_data/booltest2_tests.json', \
           short = False)
get_tests( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest2_tests_overview_short.txt', \
           dst_file_path='Cryptostreams_data/booltest2_tests_short.json', \
           short = True)
#                                                   get CFG
get_PRNG( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest2_CFGs_overview.txt', \
           dst_file_path='Cryptostreams_data/booltest2_CFGs_tests.json', \
           short = False)
get_PRNG( cryptostreams_data,  booltest_dump_gen, \
           overview_file_path='Cryptostreams_data/booltest2_CFGs_overview_short.txt', \
           dst_file_path='Cryptostreams_data/booltest2_CFGs_short.json', \
           short = True)