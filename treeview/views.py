from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
import Bio.Phylo as bp
from cStringIO import StringIO
from phylofile import settings



def list(request):
    treestore = get_treestore()

    trees = [tree_id_from_uri(uri) for uri in treestore.list_trees()]
    
    return render_to_response(
        'list.html',
        {'tree_list': trees},
        context_instance=RequestContext(request)
    )


def view(request, tree_id=None):
    treestore = get_treestore()

    tree_uri = uri_from_tree_id(tree_id)
    
    params = {
              'tree_uri': tree_uri,
              'tree_id': tree_id,
              'formats': sorted(bp._io.supported_formats.keys()) + ['ascii'],
              }
              
    tree_info = [t for t in treestore.get_tree_info(tree_uri)]
    params['tree_info'] = [(t['tree'], t['taxa']) for t in tree_info]
        
    return render_to_response(
        'view.html',
        params,
        context_instance=RequestContext(request)
    )


def download(request, tree_id=None):
    treestore = get_treestore()

    tree_uri = uri_from_tree_id(tree_id)

    if 'format' in request.GET:
        format = request.GET.get('format')
    else: format = 'newick'

    trees = treestore.get_trees(tree_uri=tree_uri)
    s = StringIO()
    if format == 'ascii':
        bp._utils.draw_ascii(trees.next(), file=s)
    else: 
        bp.write(trees, s, format)

    return download_plaintext(request, s.getvalue())


def download_plaintext(request, text, attachment=None):
    response = HttpResponse(mimetype='text/plain')
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s.%s.csv' % (site, taxon)

    response.write(text)

    return response
