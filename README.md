phylofile is a Django web application frontend to the RDF treestore, which 
stores phylogenetic trees in a triple store for easy reuse.


**Installing your own instance of phylofile**

1. To install phylofile, first install the RDF treestore:

        git clone https://https://github.com/bendmorris/rdf-treestore.git
        cd rdf-treestore
        sudo python setup.py install

2. Open phylofile/settings.py and change the following settings:

        * DOMAIN: enter your own domain name, i.e. 'http://www.example.org/'.
        * ADMINS: add a list of ('name', 'email@domain.org') tuples for each administrator.
        * TIME_ZONE, LANGUAGE_CODE: you can change these if necessary.
        * SECRET_KEY: generate your own unique secret key! This can be done with django-admin.py startproject

3. Run `python manage.py syncdb`. You'll be prompted to create a superuser 
account.