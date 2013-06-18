from django import forms
import Bio.Phylo as bp
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id


class QueryForm(forms.Form):
    treestore = get_treestore()
    
    taxa = forms.CharField(required=True,
                           initial='Homo sapiens,Pan troglodytes,Pan paniscus,Gorilla gorilla,Pongo pygmaeus',
                           widget=forms.Textarea)
    
    format_choices = sorted(bp._io.supported_formats.keys()) + ['ascii']
    format_choices = [(x,x) for x in format_choices] + [('view', 'open in tree viewer')]
    format = forms.ChoiceField(choices=format_choices,
                                initial='newick'
                               )
                               
    prune = forms.BooleanField(required=False, initial=True)
    
    match_all = forms.BooleanField(required=False, initial=False)
    
    tree_list = treestore.list_trees()
    
    tree_choices = [('', '(Select automatically)')] + [(x,x) for x in tree_list]
    tree = forms.ChoiceField(choices=tree_choices,
                             initial=tree_choices[0],
                             required=False)

    tax_choices = [('', '(None)')] + [(x,x) for x in tree_list if x.endswith('_taxonomy')]
    taxonomy = forms.ChoiceField(choices=tax_choices,
                                 initial=tax_choices[0],
                                 required=False)
                             
    filter = forms.CharField(required=False)
