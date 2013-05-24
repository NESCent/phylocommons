# if importing any of these python libraries fails, it should be cloned and installed
rdf-treestore = $(shell (echo "try:"; echo "    import treestore"; echo "    print"; echo "except:"; echo "    print 'rdf-treestore'") | python)
biopython = $(shell (echo "try:"; echo "    import Bio.Phylo"; echo "    print"; echo "except:"; echo "    print 'biopython'") | python)
python-deps = $(rdf-treestore) $(biopython)

username = 'superuser'
email = 'me@example.com'

.PHONY: all clean

all: $(python-deps) phylocommons/phylocommons.db phylocommons/settings.py

phylocommons/phylocommons.db: phylocommons/secret_key.py $(wildcard */models.py)
	python manage.py syncdb --noinput
	python manage.py createsuperuser --username $(username) --email $(email) --noinput

phylocommons/settings.py: phylocommons/secret_key.py
	# TODO: add specific user-specified settings

phylocommons/secret_key.py: generate_key.py
	python -c "from generate_key import generate_key; print('SECRET_KEY=%s' % repr(generate_key()))" \
	> phylocommons/secret_key.py

rdf-treestore:
	git clone https://github.com/bendmorris/rdf-treestore.git
	cd rdf-treestore; python setup.py install

biopython:
	git clone https://github.com/biopython/biopython.git
	cd biopython; python setup.py install

clean:
	rm -f phylocommons/phylocommons.db phylocommons/secret_key.py