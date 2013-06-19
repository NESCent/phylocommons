.PHONY: all clean ingest

all: trees

trees.rss:
	wget "http://purl.org/phylo/treebase/phylows/tree/find?query=tb.kind.tree=\"Species Tree\"&format=rss1" -O $@

trees.list: trees.rss
	grep -Po "TB2:Tr[0-9]+" trees.rss | sort | uniq > $@

trees: download_trees.py trees.list
	mkdir -p trees
	python $<

ingest: ingest_trees.py trees
	python $<

clean:
	rm -f trees.list trees.rss