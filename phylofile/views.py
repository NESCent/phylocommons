from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout


def home(request):
    return render_to_response(
        'about.html',
        context_instance=RequestContext(request)
    )

def contributors(request):
    return render_to_response(
        'contributors.html',
        context_instance=RequestContext(request)
    )

def contact(request):
    return render_to_response(
        'contact.html',
        context_instance=RequestContext(request)
    )
    
def logout(request):
    auth_logout(request)
    return redirect('/')
