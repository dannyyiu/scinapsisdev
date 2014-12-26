from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from blog.models import Post, PostImage
from django.views.generic import ListView, DetailView
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'signups.views.home', name='home'),
    url(r'^$', ListView.as_view(
            queryset=Post.objects.all().order_by("-created")[:3],
            template_name="base.html"), name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^privacy-statement/$', 'signups.views.privacy', name='privacy'),
    url(r'^blog/', include ('blog.urls', namespace='blog')),
    url(r'^contact/$', 'signups.views.contact', name='contact'),
    url(r'^coming-soon/$', 'signups.views.comingsoon', name='comingsoon'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                            document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                             document_root=settings.MEDIA_ROOT)