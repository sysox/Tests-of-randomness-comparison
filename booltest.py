from common import *
'''
tst = {
  "battery": "booltest",
  "function": "AES",
  "round": 1,
  "method": "AES-r1-e-cfg005825b630a4a94b4a19d60fc085",
  "data_bytes": 100000000,
  "deg": 1,
  "k": 1,
  "m": 128,
  "data_file": "SECMARGINPAPER27_sac_seed_874f2da1f4dabcaf_100MiB__AES_r01_b16.bin",
  "zscore": -3.7088,
  "halving": False,
  "pval0_rej": False
}
'''
'''
{
  "battery": "booltest",
  "function": "AES",
  "round": 1,
  "method": "AES-r1-e-cfg005825b630a4a94b4a19d60fc085",
  "data_bytes": 100000000,
  "deg": 1,
  "k": 1,
  "m": 128,
  "data_file": "SECMARGINPAPER27_sac_seed_874f2da1f4dabcaf_100MiB__AES_r01_b16.bin",
  "zscore": -0.274923,
  "halving": true,
  "pvalue": 0.7838099647182559,
  "pval0_rej": false
},
'''
def booltest_item_gen(item):
    res = {}
    res['exid'] = str(item['data_file'])
    res['battery'] = item['battery']
    if item['halving']:
        res['battery'] += '&halving'
    res['test'], res['subtest'], res['unitest'] = item['deg'], item['k'], item['m']
    res.update(parse_data_type(item['data_file']))
    res['pval0_rej'] = item['pval0_rej']

    return res

def booltest_dump_gen(data):
    for item in data:
        yield booltest_item_gen(item)