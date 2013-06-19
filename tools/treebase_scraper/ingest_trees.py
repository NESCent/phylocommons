import sys
import os
from treestore import Treestore


try: taxonomy = sys.argv[1]
except: taxonomy = 'itis'

t = Treestore()

tree_files = [x for x in os.listdir('trees') if x.endswith('.nex')]
base_uri = 'http://www.phylocommons.org/trees/%s'
tree_list = t.list_trees()
sys.stdout.write('Loading taxonomy...')
sys.stdout.flush()
taxonomy = t.get_trees('http://www.phylocommons.org/trees/%s_taxonomy' % taxonomy)[0]
print 'done.'

for tree_file in tree_files:
    tree_id = 'TB2_' + tree_file[:len('.nex')]
    tree_uri = base_uri % tree_id
    if tree_uri in tree_list: continue
    print '**', tree_uri
    tree_path = os.path.join('trees', tree_file)
    t.add_trees(tree_path, 'nexus', tree_uri=tree_uri, rooted=False,
                taxonomy=taxonomy, tax_root=None)
