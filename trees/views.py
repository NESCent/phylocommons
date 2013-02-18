from django.shortcuts import render_to_response
from django.http import HttpResponse
from phylofile.get_treestore import treestore
import Bio.Phylo as bp
from cStringIO import StringIO


def list(request):
    trees = treestore.list_trees()
    return HttpResponse(str(sorted([t for t in trees])))

def add(request):
    pass

def view(request, tree_uri=None):
    return render_to_response(
        'tree.html',
    )

def download(request, tree_uri=None):
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