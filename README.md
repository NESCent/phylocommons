![PhyloCommons](https://raw.github.com/bendmorris/phylocommons/master/phylocommons/static/phylocommons-logo.png)

PhyloCommons is a Django web application frontend to the RDF treestore, which 
stores phylogenetic trees in a triple store for easy reuse.


## Installing your own instance of PhyloCommons

### Django

You'll need Django version 1.4 installed. PhyloCommons uses the 
django-registration plugin which is not currently compatible with Django 1.5.

### Virtuoso

You'll also need [OpenLink Virtuoso](http://virtuoso.openlinksw.com/) installed, 
which is used to store the trees.

### Installation

Clone the repository and initialize the submodules:

    git clone https://github.com/bendmorris/phylocommons
    cd phylocommons
    git submodule init
    git submodule update

To install PhyloCommons, run `make` from the root directory. This will install
the prerequisites (rdf-treestore and biopython) if they aren't already present,
create the SQLite database, and set up the settings/secret key files.

To create a superuser account and configure the installation, pass variables 
to make:

    make username='bendmorris' email='ben@bendmorris.com'`

Variables that can be specified include:

* username: the username of the superuser (will be created without a password)
* email: the email address of the superuser
* domain: the domain the site will run from (e.g. http://www.phylocommons.org/)
* treestore_kwargs: a python dictionary of keyword arguments to be passed to the
  RDF treestore; common options are 'dsn', 'user', and 'password'

### Testing

To test PhyloCommons:

* start Virtuoso
* run `python manage.py runserver`
* navigate to localhost:8000 in your web browser