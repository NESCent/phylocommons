from django import forms
import Bio.Phylo as bp
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id


class AddTreeForm(forms.Form):
    tree_id = forms.RegexField(regex=r'^[a-zA-Z][a-zA-Z0-9\_\-]*$', min_length=10, required=True,
                               error_message='Tree ID must be at least 10 characters, start with a letter, and contain only letters, numbers, dashes and underscores.')
    
    format_choices = sorted(bp._io.supported_formats.keys())
    format_choices = [(x,x) for x in format_choices]
    format = forms.ChoiceField(choices=format_choices,
                                initial='newick'
                               )
                               
    tree_file  = forms.FileField()
