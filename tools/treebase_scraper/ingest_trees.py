#!/usr/bin/env python
import sys
import os
from treestore import Treestore


try: taxonomy = sys.argv[1]
except: taxonomy = None

t = Treestore()

tree_files = [x for x in os.listdir('trees') if x.endswith('.nex')]
base_uri = 'http://www.phylocommons.org/trees/%s'
tree_list = set(t.list_trees())
if taxonomy:
    sys.stdout.write('Loading taxonomy...')
    sys.stdout.flush()
    taxonomy = t.get_trees('%s_taxonomy' % taxonomy)[0]
    taxonomy.index_labels()
    print 'done.'

errors = set()
for tree_file in tree_files:
    tree_id = 'TB2_' + tree_file[:-len('.nex')]
    if tree_id in tree_list: continue
    print '**', tree_id
    tree_path = os.path.join('trees', tree_file)
    with open(tree_path) as input_file:
        r = input_file.read()
    if '<!DOCTYPE html' in r: continue
    try:
        t.add_trees(tree_path, 'nexus', tree_uri=tree_id, rooted=False,
                    taxonomy=taxonomy, tax_root=None)
    except Exception as e:
        print 'ERROR: ', e
        errors.add(tree_id)

if errors:
    print "Couldn't load the following trees:", ','.join(errors)