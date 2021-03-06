from django import forms
import Bio.Phylo as bp
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from phylocommons import settings


class QueryForm(forms.Form):
    with get_treestore() as treestore:
        taxa = forms.CharField(required=True,
                               widget=forms.Textarea)
        taxa.widget.attrs['class'] = 'stretch'
        taxa.widget.attrs['placeholder'] = 'Enter a comma-separated list of taxa (e.g. Homo sapiens,Pan troglodytes,Pan paniscus,Gorilla gorilla,Pongo pygmaeus) to build a tree containing those taxa'
        
        format_choices = sorted(bp._io.supported_formats.keys()) + ['ascii']
        format_choices = [('view', '(open in tree viewer)')] + [(x,x) for x in format_choices]
        format = forms.ChoiceField(choices=format_choices,
                                   initial=format_choices[0],
                                   )
        format.widget.attrs['class'] = 'stretch'
                                   
        prune = forms.BooleanField(required=False, initial=True)
        
        tree_list = [tree_id_from_uri(x) for x in treestore.list_trees()]
        
        tree_choices = [('', '(see all matching trees)'),
                        ('best', '(choose the best match)')] + [(x,x) for x in tree_list]
        tree = forms.ChoiceField(choices=tree_choices,
                                 initial=tree_choices[0],
                                 required=False)
        tree.widget.attrs['class'] = 'combobox'

        tax_choices = [('', '(None)')] + [(x,x) for x in tree_list if x.endswith('_taxonomy')]
        taxonomy = forms.ChoiceField(choices=tax_choices,
                                     initial=settings.DEFAULT_TAXONOMY,
                                     required=False)
        taxonomy.widget.attrs['class'] = 'combobox'
                                 
        filter = forms.CharField(required=False)
        filter.widget.attrs['class'] = 'stretch'
