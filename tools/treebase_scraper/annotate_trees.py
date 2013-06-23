#!/usr/bin/env python
import sys
import os
from treestore import Treestore


try: taxonomy = sys.argv[1]
except: taxonomy = None

t = Treestore()

treebase_uri = 'http://purl.org/phylo/treebase/phylows/tree/%s'

tree_files = [x for x in os.listdir('trees') if x.endswith('.nex')]
base_uri = 'http://www.phylocommons.org/trees/%s'
tree_list = set(t.list_trees())
for tree_uri in tree_list:
    if not 'TB2_' in tree_uri: continue
    tree_id = t.id_from_uri(tree_uri)
    tb_uri = treebase_uri % (tree_id.replace('_', ':'))
    print tree_id, tb_uri
    t.annotate(tree_uri, annotations='?tree bibo:cites <%s> .' % tb_uri)
