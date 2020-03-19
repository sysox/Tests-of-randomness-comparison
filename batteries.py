from common import *
from my_tree import *

def batteries_item_gen(item):
    res = {}
    res['exid'] = str(item['exid'])
    res['battery'], res['test'] = item['test'].split('|')
    subtest = 'sub:' + item['subtest'] + ' var:'+item['variant']
    res.update(parse_data_type(item['data_type']))
    res['data_type'] = item['data_type']
    for dic_1 in item['subs']:
        res['subtest'] = subtest
        if 'idx' in dic_1:
            res['subtest'] += ' idx:' + str(dic_1["idx"])
        for dic_2 in dic_1['stats']:
            res['unitest'] = dic_2['name']
            res['p-val'] = dic_2['value']
            yield res

def batteries_dump_gen(data):
    for results in data:
        for item_dic in batteries_item_gen(results):
           yield item_dic

