from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
import Bio.Phylo as bp
from cStringIO import StringIO


def query(request):
    treestore = get_treestore()
    
    query = None
    format = 'newick'
    prune = True
    
    if request.method == 'POST':
        query = request.POST.get('q')
        if 'format' in request.POST: format = request.POST.get('format')
        if 'prune' in request.POST: prune = request.POST.get('prune')[0].lower() == 'y'
        
    elif request.method == 'GET':
        if 'q' in request.GET:
            query = request.GET.get('q')
            if 'format' in request.POST: format = request.POST.get('format')
            if 'prune' in request.POST: prune = request.POST.get('prune')[0].lower() == 'y'
            
    if not query is None:
        taxa = query
        contains = taxa.split(',')
            
        trees = treestore.get_subtree(contains=contains, format=format, prune=prune)
            
        return download_plaintext(request, trees)
            
            
    params = {
              'formats': sorted(bp._io.supported_formats.keys()) + ['ascii'],
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
