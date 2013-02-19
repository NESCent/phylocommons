from django.shortcuts import render_to_response
from django.http import HttpResponse
from phylofile.get_treestore import get_treestore
from treestore import Treestore
import Bio.Phylo as bp
from cStringIO import StringIO



def list(request):
    treestore = get_treestore()

    trees = treestore.list_trees()
    
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


def view(request, tree_uri=None):
    treestore = get_treestore()
    
    params = {
              'tree_uri': tree_uri,
              'download_formats': sorted(bp._io.supported_formats.keys()) + ['ascii'],
              }
              
    tree_info = [t for t in treestore.get_tree_info(tree_uri)]
    params['tree_info'] = [(t['tree'], t['taxa']) for t in tree_info]
        
    if 'names' in request.GET and request.GET.get('names').lower()[0] == 'y':
        names = treestore.get_names(tree_uri)
        params['names'] = names

    return render_to_response(
        'view.html',
        params
    )


def download(request, tree_uri=None):
    treestore = get_treestore()

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
