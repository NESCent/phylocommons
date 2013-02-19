from django import forms
import Bio.Phylo as bp
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id


class AddTreeForm(forms.Form):
    taxa = forms.CharField(required=True)
    
    format_choices = sorted(bp._io.supported_formats.keys())
    format_choices = [(x,x) for x in format_choices]
    format = forms.ChoiceField(choices=format_choices,
                                initial='newick'
                               )
                               
    tree_file  = forms.FileField()
