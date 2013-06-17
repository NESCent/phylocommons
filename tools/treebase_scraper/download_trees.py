import os
import sys
import urllib2

nexus_url = "http://purl.org/phylo/treebase/phylows/tree/%s?format=nexus"

with open('trees.list') as tree_list:
    for line in tree_list:
        tree_id = line.strip()

        tree_file = 'trees/%s.nex' % tree_id.split(':')[-1]
        if os.path.exists(tree_file): continue

        sys.stdout.write('Downloading %s ...' % tree_id)
        sys.stdout.flush()
        source = urllib2.urlopen(nexus_url % tree_id)

        with open(tree_file, 'w') as output_file:
            data = source.read(1024)
            while data:
                output_file.write(data)
                data = source.read(1024)

        print 'done!'
