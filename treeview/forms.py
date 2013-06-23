from django import forms
import Bio.Phylo as bp
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id


class SearchForm(forms.Form):
    taxa = forms.CharField(required=False)
    taxa.widget.attrs['class'] = 'search-query'
    taxa.widget.attrs['placeholder'] = 'Search for taxa'
                             
    filter = forms.CharField(required=False)
    #filter.widget.attrs['class'] = 'stretch'
    filter.widget.attrs['placeholder'] = 'SPARQL filter'
