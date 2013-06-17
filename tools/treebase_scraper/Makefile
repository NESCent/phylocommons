all: trees.list

trees.rss:
	wget "http://purl.org/phylo/treebase/phylows/tree/find?query=tb.kind.tree=\"Species Tree\"&format=rss1" -O $@

trees.list: trees.rss
	grep -Po "TB2:Tr[0-9]+" trees.rss | sort | uniq > $@

trees: 
	mkdir -p trees
	python download_trees.py

clean:
	rm -f trees.list trees.rss