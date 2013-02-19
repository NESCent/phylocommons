from django.shortcuts import render_to_response
from django.http import HttpResponse
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
import Bio.Phylo as bp
from cStringIO import StringIO



def list(request):
    treestore = get_treestore()

    trees = [tree_id_from_uri(uri) for uri in treestore.list_trees()]
    
    return render_to_response(
        'list.html',
        {'tree_list': trees}
    )


def add(request):
    if request.method == 'POST':
        pass

    return render_to_response(
        'add.html',
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
        
    if 'names' in request.GET and request.GET.get('names')[0].lower() == 'y':
        names = treestore.get_names(tree_uri)
        params['names'] = names

    return render_to_response(
        'view.html',
        params
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
