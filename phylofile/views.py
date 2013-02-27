from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User


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
    
def user_profile(request, user_id):
    try:
        this_user = User.objects.get(username=user_id)
    except:
        this_user = None
    
    return render_to_response(
        'user_profile.html',
        {'user': this_user},
        context_instance=RequestContext(request)
    )
