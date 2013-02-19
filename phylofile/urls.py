from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'phylofile.views.home', name='home'),
    url(r'^about/$', 'phylofile.views.about', name='about'),
    url(r'^contributors/$', 'phylofile.views.about', name='contributors'),
    url(r'^contact/$', 'phylofile.views.about', name='contact'),
    
    # trees application (add, get, etc.)
    url(r'^trees/', include('trees.urls')),

    # treequery application
    url(r'^trees/', include('treequery.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
