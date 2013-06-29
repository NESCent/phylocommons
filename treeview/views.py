from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from forms import SearchForm
import Bio.Phylo as bp
from cStringIO import StringIO
from phylocommons import settings
import urllib
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.http import Http404
cdao_elements = bp._cdao_owl.cdao_elements
obo_to_cdao = {v:k for k,v in cdao_elements.items()}


TREES_PER_PAGE = 10

def tree_list(request):
    treestore = get_treestore()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            taxa = form.cleaned_data['taxa']
            filter = form.cleaned_data['filter']
            params = [(x, y) for x, y in form.cleaned_data.items()]
            return redirect('/trees/?' + urllib.urlencode(params))
    else:    
        taxa = request.GET.get('taxa')
        filter = request.GET.get('filter')
        filter = filter if filter else None

        form = SearchForm(initial=request.GET)
        form.full_clean()

    taxa = [x.strip() for x in taxa.split(',')] if taxa else []
    
    params = {'form': form, 'taxonomy':settings.DEFAULT_TAXONOMY}
    params.update(csrf(request))
    
    try:
        trees = list(treestore.list_trees_containing_taxa(contains=taxa, filter=filter, 
                        taxonomy=settings.DEFAULT_TAXONOMY, show_counts=True))
    except Exception as e:
        errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
        err_msg = "There was a problem with your search: %s" % e
        errors.append(err_msg)
        
        return render_to_response(
            'list.html',
            params,
            context_instance=RequestContext(request)
        )
        
    trees = [(tree_id_from_uri(m[0]), int(m[1])) for m in trees]
    paginator = Paginator(trees, TREES_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        tree_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tree_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tree_list = paginator.page(paginator.num_pages)
    
    params.update({'tree_list': tree_list,
                   'max_match_count': len(taxa)})

    num_pages = paginator.num_pages
    page_range = [n for n in range(tree_list.number - 2, tree_list.number + 3) 
                  if n >= 1 and n <= num_pages]

    params.update({
        'total_results': len(trees),
        'low_result': TREES_PER_PAGE * (tree_list.number - 1) + 1,
        'high_result': min(len(trees), TREES_PER_PAGE * tree_list.number)
        })
    
    if page_range[0] == 2: page_range = [1] + page_range
    elif page_range[0] > 2: page_range = [1, '...'] + page_range
    
    if page_range[-1] == num_pages - 1: page_range += [num_pages]
    elif page_range[-1] < num_pages - 1: page_range += ['...', num_pages]
    
    pages = []
    
    for page in page_range:
        if page == '...': pages.append((page, None))
        else:
            p = []
            for arg in ('taxa', 'filter'):
                if arg in request.GET:
                    p += [(arg, request.GET.get(arg))]
            p += [('page', page)]
            pages.append((page, '/trees/?' + urllib.urlencode(p)))
    
    params['pages'] = pages
    
    return render_to_response(
        'list.html',
        params,
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
              
    try:
        all_tree_info = treestore.get_tree_info(tree_uri)
        tree_info = {}
        tree_info.update(all_tree_info[0])
        tree_info['citation'] = []
        for x in all_tree_info:
            if x['citation']: tree_info['citation'].append(x['citation'])
    except IndexError:
        raise Http404
        return not_found(request, tree_uri)
    obj_info = treestore.get_object_info(tree_uri)
    prefixes = treestore.prefixes
    def add_prefix(x):
        for prefix, uri in prefixes:
            if x.startswith(uri):
                if prefix == 'obo':
                    try: return 'cdao:%s' % (obo_to_cdao[x[len(uri):]])
                    except: pass
                return '%s:%s' % (prefix, x[len(uri):])
        return x
    obj_info = [sum([(x, add_prefix(x)) for x in row], ()) for row in obj_info]
    print obj_info
    
    params.update(tree_info)
    params['obj_info'] = obj_info
        
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

    if format == 'taxa_list':
        # download list of taxa
        names = treestore.get_names(tree_uri)
        spp_list = ','.join(names)
        return download_plaintext(request, spp_list)

    trees = treestore.get_trees(tree_uri=tree_uri)
    s = StringIO()
    if format == 'ascii':
        bp._utils.draw_ascii(trees[0], file=s)        
    else: 
        bp.write(trees, s, format)

    return download_plaintext(request, s.getvalue())


def download_plaintext(request, text, attachment=None):
    response = HttpResponse(mimetype='text/plain')
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s.%s.csv' % (site, taxon)

    response.write(text)

    return response
    
    
def svgview(request, tree_id, tree_src=None):
    treestore = get_treestore()
    
    if not tree_src: tree_src = '/trees/%s/download?format=newick' % tree_id
    
    return render_to_response(
        'svgview.html',
        {'tree_src': tree_src, 'tree_id': tree_id, 'tree_uri': uri_from_tree_id(tree_id)},
        context_instance=RequestContext(request)
    )
