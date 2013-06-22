from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.template import RequestContext
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from treequery.forms import QueryForm
import Bio.Phylo as bp
from cStringIO import StringIO
from phylocommons import settings
import treeview.views
import urllib


def query(request):
    treestore = get_treestore()
    
    format = 'newick'
    prune = True
    tree_uri = None
    tree_id = None
    filter = None
    taxonomy = None
    
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            submitted_query = True
            taxa = form.cleaned_data['taxa']
            prune = form.cleaned_data['prune']
            format = form.cleaned_data['format']
            tree_id = form.cleaned_data['tree']
            taxonomy = form.cleaned_data['taxonomy']
            filter = form.cleaned_data['filter']
        else:
            submitted_query = False
        
    elif request.method == 'GET' and 'taxa' in request.GET:
        submitted_query = True
        taxa = request.GET.get('taxa')
        if 'format' in request.GET: format = request.GET.get('format')
        if 'prune' in request.GET: prune = request.GET.get('prune')[0].lower() == 'y'
        if 'tree' in request.GET: tree_id = request.GET.get('tree')
        if 'taxonomy' in request.GET: taxonomy = request.GET.get('taxonomy')
        if 'filter' in request.GET: filter = request.GET.get('filter')
            
    else:
        submitted_query = False
        form = QueryForm()
            

    if submitted_query:
        if format == 'view':
            tree_src = '/query/?' + urllib.urlencode([
                (a, b) for (a, b) in
                [
                ('format', 'newick'),
                ('prune', 'y' if prune else 'n'),
                ('taxa', taxa),
                ('tree', tree_id),
                ('taxonomy', taxonomy),
                ('filter', filter),
                ]
                if b]
                )
            print tree_src
            return treeview.views.svgview(request, 
                tree_src=tree_src)
        
        if tree_id: tree_uri = uri_from_tree_id(tree_id)
        if taxonomy: taxonomy = uri_from_tree_id(taxonomy)

        # execute the query and return the result as a plaintext tree
        contains = [t.strip() for t in taxa.split(',')]
        
        if tree_uri is None:
            # 'select automatically' was chosen; perform the disambiguation step
            # if there are more than one matching tree
            trees = None
            matches = []
            for match in treestore.list_trees_containing_taxa(contains=contains, 
                                                              show_counts=False,
                                                              filter=filter):
                matches.append(match)
                if len(matches) > 10: break
            
            if len(matches) == 1:
                try:
                    trees = treestore.get_subtree(contains=contains, tree_uri=matches[0],
                                                  format=format, prune=prune, filter=filter,
                                                  taxonomy=taxonomy)
                except Exception as e:
                    trees = None
                    exception = e
                    
            elif len(matches) > 1:
                return query_disambiguate(request, matches)
                
        else:
            try:
                trees = treestore.get_subtree(contains=contains, tree_uri=tree_uri,
                                              format=format, prune=prune, filter=filter,
                                              taxonomy=taxonomy)
            except Exception as e:
                trees = None
                exception = e
                
        if trees:
            return download_plaintext(request, trees)
            
        else:
            
            errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
            errors.append('%s' % e)
            
            err_msg = "Your query didn't return a result. Try entering a new list of taxa"
            if tree_uri: err_msg += ' or selecting a different tree'
            err_msg += '.'
            errors.append(err_msg)
        
        
    # show the query builder page
            
    params = {
              'form': form,
              'domain': settings.DOMAIN.rstrip('/'),
              'tree_uri': settings.TREE_URI,
              }
    params.update(csrf(request))
            
    return render_to_response(
        'query.html',
        params,
        context_instance=RequestContext(request)
    )

            

def query_disambiguate(request, matches):
    #TODO
    return render_to_response(
        'disambiguate.html',
        params,
        context_instance=RequestContext(request)
    )


def download_plaintext(request, text, attachment=None):
    response = HttpResponse(mimetype='text/plain')
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s.%s.csv' % (site, taxon)

    response.write(text)

    return response
