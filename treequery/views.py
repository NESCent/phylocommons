from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.template import RequestContext
from phylocommons.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from treeview.views import download_plaintext
from treequery.forms import QueryForm
import Bio.Phylo as bp
from cStringIO import StringIO
from phylocommons import settings
import treeview.views
import urllib
import sys


MAX_DISAMBIG_MATCHES = 10

def query(request):
    with get_treestore() as treestore:
        tree_uri = None
        params = {
            'taxa': '',
            'format': 'newick',
            'prune': True,
            'tree_id': None,
            'filter': None,
            'taxonomy': None,
            }
        
        if request.method == 'POST':
            form = QueryForm(request.POST)
            if form.is_valid():
                url = '/query/?' + urllib.urlencode(form.cleaned_data.items())
                if len(url) < 200: return redirect(url)
                params.update(form.cleaned_data)
                submitted_query = True
            else:
                submitted_query = False
            
        elif request.method == 'GET' and 'taxa' in request.GET:
            submitted_query = True
            taxa = request.GET.get('taxa')
            params.update(request.GET.dict())
            if 'prune' in request.GET: params['prune'] = params['prune'] == 'True'
            form = QueryForm(initial=request.GET.dict())
            form.full_clean()
            
        else:
            submitted_query = False
            form = QueryForm(initial=request.GET.dict())
        

        best_match = params['tree_id'] == 'best'
        
        if submitted_query:
            if best_match: tree_uri = None
            else: tree_uri = uri_from_tree_id(params['tree_id']) if params['tree_id'] else None
            taxonomy = uri_from_tree_id(params['taxonomy']) if params['taxonomy'] else None
            
            if params['format'] == 'view' and tree_uri:
                params['format'] = 'newick'
                tree_src = '/query/?' + urllib.urlencode(params.items())

                return treeview.views.svgview(request, params['tree_id'], tree_src=tree_src)
            
            # execute the query and return the result as a plaintext tree
            contains = [t.strip() for t in params['taxa'].split(',')]
            
            e = None
            response = None
            
            if tree_uri is None:
                # 'select automatically' was chosen; perform the disambiguation step
                # if there are more than one matching tree
                trees = None
                matches = []
                try:
                    for match in treestore.list_trees_containing_taxa(contains=contains, 
                                                                      show_counts=True,
                                                                      taxonomy=taxonomy,
                                                                      filter=params['filter']):
                        if int(match[1]) < 2 and params['prune']:
                            if not matches:
                                raise Exception("The top match only matched one taxon, which isn't enough to make a tree. Try unchecking the 'prune results' checkbox.")
                            break
                        matches.append((match[0], int(match[1])))
                        if len(matches) >= (1 if best_match else MAX_DISAMBIG_MATCHES): break

                except Exception as e:
                    trees = None
                
                if matches and not e:
                    if best_match:
                        if params['format'] == 'view':
                            params['format'] = 'newick'
                            params['tree_id'] = matches[0][0]
                            tree_src = '/query/?' + urllib.urlencode(params.items())

                            return treeview.views.svgview(request, tree_id_from_uri(matches[0][0]), 
                                                          tree_src=tree_src)

                        response = HttpResponse(mimetype='text/plain')
                        sys.stdout = response
                        trees = treestore.get_subtree(contains=contains,
                                                      tree_uri=matches[0][0],
                                                      format=params['format'],
                                                      prune=params['prune'],
                                                      filter=params['filter'],
                                                      taxonomy=taxonomy)
                        sys.stdout = sys.__stdout__
                    else: return query_disambiguate(request, matches, params)
                elif not e:
                    trees = None
                    e = 'There were no trees that matched your query.'
                
                    
            else:
                try:
                    response = HttpResponse(mimetype='text/plain')
                    sys.stdout = response
                    trees = treestore.get_subtree(contains=contains,
                                                  tree_uri=tree_uri,
                                                  format=params['format'],
                                                  prune=params['prune'],
                                                  filter=params['filter'],
                                                  taxonomy=taxonomy)
                    sys.stdout = sys.__stdout__
                except Exception as e:
                    trees = None
                    exception = e
                    
            if trees:
                if response: return download_plaintext(request, response=response)
                return download_plaintext(request, trees)
                
            else:
                errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                if e:
                    errors.append('There was a problem with your query: %s' % e)
                else:
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

            

def query_disambiguate(request, matches, form_fields):
    if 'tree_id' in form_fields: del form_fields['tree_id']
    matches = [(tree_id_from_uri(m[0]), m[1]) for m in matches]
    params = {'tree_list': matches, 
              'max_match_count': len(form_fields['taxa'].split(',')), 
              'form_fields': form_fields}

    params.update(csrf(request))

    return render_to_response(
        'disambiguate.html',
        params,
        context_instance=RequestContext(request)
    )
