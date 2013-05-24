# if importing any of these python libraries fails, it should be cloned and installed
biopython = $(shell (echo "try:"; echo "    import Bio.Phylo"; echo "    print"; echo "except:"; echo "    print 'biopython'") | python)
rdf-treestore = $(shell (echo "try:"; echo "    import treestore"; echo "    print"; echo "except:"; echo "    print 'rdf-treestore'") | python)
python-deps = $(biopython) $(rdf-treestore)

# superuser name and email
username = 'superuser'
email = 'me@example.com'
# web application domain
domain = 'http://www.phylocommons.org/'
# 
treestore_kwargs = {}

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
	git clone https://github.com/bendmorris/rdf-treestore.git
	cd rdf-treestore; python setup.py install

biopython:
	git clone https://github.com/biopython/biopython.git
	cd biopython; python setup.py install

clean:
	rm -f phylocommons/phylocommons.db phylocommons/secret_key.py