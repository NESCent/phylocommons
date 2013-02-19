from django import forms
import Bio.Phylo as bp
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id


class QueryForm(forms.Form):
    treestore = get_treestore()
    
    taxa = forms.CharField(required=True,
                           initial='Homo sapiens,Pan troglodytes,Gorilla gorilla,Pongo pygmaeus',
                           widget=forms.Textarea)
    
    format_choices = ['ascii'] + sorted(bp._io.supported_formats.keys())
    format_choices = [(x,x) for x in format_choices]
    format = forms.ChoiceField(choices=format_choices,
                                initial='newick'
                               )
                               
    prune = forms.BooleanField(required=False, initial=True)
    
    tree_choices = [t for t in treestore.list_trees()]
    tree_choices = [('', '(Select automatically)')] + [(x,x) for x in tree_choices]
    tree = forms.ChoiceField(choices=tree_choices,
                             initial=tree_choices[0],
                             required=False)
                             
    filter = forms.CharField(required=False)
