from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
import Bio.Phylo as bp
from cStringIO import StringIO
from phylocommons import settings



def list(request):
    treestore = get_treestore()
    
    trees = [tree_id_from_uri(uri) for uri in treestore.list_trees()]
    paginator = Paginator(trees, 25) # Show 25 contacts per page
    
    page = request.GET.get('page')
    try:
        tree_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tree_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tree_list = paginator.page(paginator.num_pages)
    
    return render_to_response(
        'list.html',
        {'tree_list': tree_list},
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
              
    tree_info = treestore.get_tree_info(tree_uri)[0]
    params.update(tree_info)
        
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
    
    
def svgview(request, tree_id=None, tree_src=None):
    treestore = get_treestore()
    
    if tree_id: tree_src = '/trees/%s/download?format=newick' % tree_id
    
    return render_to_response(
        'svgview.html',
        {'tree_src': tree_src},
        context_instance=RequestContext(request)
    )
