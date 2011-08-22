from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse # for hacky one-liner
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # pro forma
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # render static and media content as per MEDIA_ROOT and STATIC_ROOT
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # userena account urls
    (r'^accounts/', include('userena.urls')),
    # Utility urls
    url(r'^load$', 'schooldash.dataload.views.load_demographics'),
    # Application urls
    (r'^all_demo$', 'schooldash.datashow.views.show_all', {'demo': True}),
    (r'^all$', 'schooldash.datashow.views.show_all', {'demo': False}),
    url(r'^class$', 'schooldash.datashow.views.show_class'),

    # sort of hacky one-liner to generate a robots.txt (breaks MTV, but w/e)
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain")),
)
