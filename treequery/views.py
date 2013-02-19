from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from treequery.forms import QueryForm
import Bio.Phylo as bp
from cStringIO import StringIO


def query(request):
    treestore = get_treestore()
    
    query = None
    format = 'newick'
    prune = True
    tree_uri = None
    
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['taxa']
            prune = form.cleaned_data['prune']
            format = form.cleaned_data['format']
            tree_uri = form.cleaned_data['tree']
        
    elif request.method == 'GET' and 'q' in request.GET:
            query = request.GET.get('q')
            if 'format' in request.GET: format = request.GET.get('format')
            if 'prune' in request.GET: prune = request.GET.get('prune')[0].lower() == 'y'
            if 'tree' in request.GET: tree_uri = request.GET.get('tree')
            
    else:
        form = QueryForm()
            

    if not query is None:
        # execute the query and return the result as a plaintext tree
        taxa = query
        contains = taxa.split(',')
        
        trees = treestore.get_subtree(contains=contains, tree_uri=tree_uri,
                                      format=format, prune=prune)
            
        return download_plaintext(request, trees)
        
        
    # show the query builder page
            
    params = {
              'form': form,
              }
    params.update(csrf(request))
            
    return render_to_response(
        'query.html',
        params
    )

            
def download_plaintext(request, text, attachment=None):
    response = HttpResponse(mimetype='text/plain')
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s.%s.csv' % (site, taxon)

    response.write(text)

    return response
