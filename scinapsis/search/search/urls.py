from django.conf.urls import patterns, url, include, static
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from search import views
admin.autodiscover()

urlpatterns = patterns('',
        (r'^accounts/', include('allauth.urls')),
        (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
        )

urlpatterns += patterns('search.views',

    # url(r'^$', 'login_view'),
    # url(r'^login/$', 'login_view', name='login'),
    # url(r'^/?$', 'index', name='home'),
    url(r'^$', 'dashboard'),
    url(r'^dash/?$', 'dashboard', name='dash'),
    url(r'^list/?$', 'index', name='index'),
    url(r'^view/([0-9]+)/?$', 'view', name='view'),
    url(r'^figureview/([0-9]+)/?$', 'figure_view', name='figureview'),
    url(r'^logout/?$', 'logout_view'),
    url(r'^admin/?', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^userprofile/?', include('userprofile.urls', namespace="userprofile")),
    url(r'^typeahead-search/?', views.typeahead_view, name="typeahead_search")
    
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                            document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                             document_root=settings.MEDIA_ROOT)
