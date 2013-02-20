from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from treeupload.forms import TreeSubmissionForm
import Bio.Phylo as bp
from cStringIO import StringIO
from phylofile import settings



def add(request):
    if request.method == 'POST':
        form = TreeSubmissionForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TreeSubmissionForm()
    
    params = {
              'form': form,
              'domain': settings.DOMAIN.rstrip('/'),
              }
    params.update(csrf(request))
    
    return render_to_response(
        'add.html',
        params
    )
