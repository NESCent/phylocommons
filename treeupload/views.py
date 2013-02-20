from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from phylofile.get_treestore import get_treestore, tree_id_from_uri, uri_from_tree_id
from treeupload.models import TreeSubmission
from treeupload.forms import TreeSubmissionForm
import Bio.Phylo as bp
from cStringIO import StringIO
from phylofile import settings



def add(request):
    if request.method == 'POST':
        form = TreeSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            newtree = TreeSubmission(tree_file = request.FILES['tree_file'],
                                     format=request.POST.get('format'),
                                     tree_id=request.POST.get('tree_id'),
                                     uploaded_by=request.user)
            newtree.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('treeupload.views.add'))

    else:
        form = TreeSubmissionForm()
    
    params = {
              'form': form,
              'domain': settings.DOMAIN.rstrip('/'),
              }
    params.update(csrf(request))
    
    return render_to_response(
        'add.html',
        params,
        context_instance=RequestContext(request)
    )
    
    
def uploads(request):
    #if request.method == 'POST':
    #    selected_documents = ','.join(request.POST.getlist('document-selector'))
    #    
    #    print repr(selected_documents)
    #
    #    if selected_documents:
    #        newjob = ProcessingJob(user=request.user, documents=selected_documents)
    #        newjob.save()
    #        
    #    return HttpResponseRedirect(reverse('sp_list.views.jobs'))
    
    files = TreeSubmission.objects.all()
    
    return render_to_response(
        'uploads.html',
        {
         'files': files,
        },
        context_instance=RequestContext(request)
    )
