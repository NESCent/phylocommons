# superuser name and email (note that these are interpreted as python 
# expressions, so the quotes are significant)
username = 'superuser'
email = 'me@example.com'
# web application domain
domain = 'http://www.phylocommons.org/'
# python dictionary of keyword arguments for treestore connection
# example: {'dsn':'Virtuoso', 'user':'dba', 'password':'dba'}
treestore_kwargs = {}

# if importing any of these python libraries fails, it should be cloned and installed
biopython = $(shell (echo "try:"; echo "    import Bio.Phylo"; echo "    print"; echo "except:"; echo "    print 'biopython'") | python)
phylolabel = $(shell (echo "try:"; echo "    import phylolabel"; echo "    print"; echo "except:"; echo "    print 'phylolabel'") | python)
rdf-treestore = $(shell (echo "try:"; echo "    import treestore"; echo "    print"; echo "except:"; echo "    print 'rdf-treestore'") | python)
python-deps = $(biopython) $(phylolabel) $(rdf-treestore)

.PHONY: all clean

all: $(python-deps) phylocommons/phylocommons.db phylocommons/settings.py

phylocommons/phylocommons.db: phylocommons/secret_key.py $(wildcard */models.py)
	python manage.py syncdb --noinput
	python manage.py createsuperuser --username $(username) --email $(email) --noinput

phylocommons/settings.py: phylocommons/secret_key.py phylocommons/settings_template.py
	(echo "ADMINS = (($(username), $(email)))"; \
	 echo "DOMAIN = $(domain)"; \
	 echo "TREESTORE_KWARGS = $(treestore_kwargs)"; \
	 cat phylocommons/settings_template.py) \
	> $@

phylocommons/secret_key.py: generate_key.py
	python -c "from generate_key import generate_key; print('SECRET_KEY=%s' % repr(generate_key()))" \
	> $@

rdf-treestore:
	cd tools/rdf-treestore; python setup.py install

phylolabel:
	cd tools/phylolabel; python setup.py install

biopython:
	git clone https://github.com/biopython/biopython.git
	cd biopython; python setup.py install

clean:
	rm -f phylocommons/phylocommons.db phylocommons/secret_key.py phylocommons/settings.py