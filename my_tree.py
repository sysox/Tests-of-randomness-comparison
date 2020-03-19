import collections
from common import *
import copy
import itertools
import sys

def get_node(tree, keys):
    node = tree
    for key in keys:
        node = node[key]
    return node

def add_branch(tree, keys, container_type = dict):
    node = tree
    for key in keys[:-1]:
        if key not in node:
            node[key] = {}
        node = node[key]

    if container_type == dict:
        return node

    if keys[-1] not in node:
        node[keys[-1]] = container_type()
    return node[keys[-1]]

def add_value(tree, keys, value, container_type = dict):
    """  """
    node = add_branch(tree, keys, container_type)
    if isinstance(node, list):
        node.append(value)
    elif isinstance(node, set):
        node.add(value)
    else:
        node[keys[-1]] = value

def traverse(tree, keys = [], depth = 0, all = False):
    node = tree
    if  depth == 0 or not isinstance(node, collections.Iterable) or isinstance(node, str):
        yield node, keys
        return
    elif all == True:
        yield node, keys
    if isinstance(node, collections.Mapping):
        for key in sorted(node.keys()):
            if key == 'count':
                continue
            yield from traverse(node[key], keys + [key], depth - 1, all)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            yield from traverse(node[idx], keys + [idx], depth - 1, all)
    elif isinstance(node, set):
        for item in node:
            yield from traverse(item, keys, depth - 1, all)

SIZE_KEY = 'SIZE'

def counts_nodes(tree):
    for node, keys in traverse(tree, keys = [], depth = -1, all = False):
        if isinstance(node, collections.abc.Mapping):
            node.pop(SIZE_KEY, None)
    if not isinstance(tree, collections.Mapping):
        if  not isinstance(tree, list) and not isinstance(tree, set):
            return [1]
        else:
            return [len(tree)]
    if SIZE_KEY in tree:
        return tree[SIZE_KEY]
    counts = []
    for key in tree.keys():
        if key == SIZE_KEY:
            continue
        tmp_counts = counts_nodes(tree[key])
        counts = [sum(x) for x in itertools.zip_longest(counts, tmp_counts, fillvalue=0)]
    tree[SIZE_KEY] = [len(tree)] + counts
    return tree[SIZE_KEY]


def sorted_by_size(node):
    keys = list(set(node.keys()) - set([SIZE_KEY]))
    sorted_key = sorted(keys, reverse=True, key=lambda key: node[key][SIZE_KEY][-1] if isinstance(node[key], collections.Mapping) else len(node[key]))
    # for key in node.keys():
    #     if isinstance(node[key], collections.Mapping):
    #         print(node[key][SIZE_KEY])
    #     else:
    #         print(len(node[key]))
    for key in sorted_key:
        yield key

def print_tree(node, key = None, lvl = 0, max_lvl = -1, row = False, file_name = '', path='/mnt/c/sysox/DATA/',  ):
    if file_name:
        sys.stdout = open(path + file_name, 'w')

    if max_lvl == lvl:
        return

    if key == None:
        key = 'root'

    #leaf
    if not isinstance(node, collections.abc.Iterable) or isinstance(node, str):
        print(lvl * '\t' + '%s %s %s' % (key, node, [1]))
        return

    elif isinstance(node, collections.Mapping):
        print(lvl * '\t' + '%s %s' % (key, node[SIZE_KEY]))
        # for key in node:
        for key in sorted_by_size(node):
            if key == SIZE_KEY:
                continue
            print_tree(node[key], key, lvl + 1, max_lvl)

    elif isinstance(node, list) or isinstance(node, set):
        print(lvl * '\t' + '%s %s' % (key, [len(node)]))
        for idx, value in enumerate(node):
            print_tree(value, idx, lvl + 1, max_lvl)
            # print(json.dumps(node, indent=4, cls=CustomJsonEncoder))

        # if row == True:
        # print((lvl+1) * '\t' + '%s' % (sorted(map(float, node))))
    if file_name:
        sys.stdou = sys.__stdout__

def join_trees(tree1, tree2, container_type):
    for value, keys in traverse(tree2, [], -1, False):
        # print(value, keys)
        add_value(tree1, keys, value, container_type)
    return tree1

if __name__ == "__main__":
    tree1 = {}
    add_value(tree1, [1,2], 3, list)
    add_value(tree1, [1,2], 4, list)
    counts_nodes(tree1)
    print_tree(tree1, None,0, 4)