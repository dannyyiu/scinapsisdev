from django.conf.urls import patterns, url
from django.views.generic import ListView
from blog.models import Post
from django.contrib.syndication.views import Feed
from blog.views import PostDetailView, PostIndexView

class BlogFeed(Feed):
    title = "MySite"
    description = "Some ramblings of mine"
    link = "/blog/feed/"

    def items(self):
        return Post.objects.all().order_by("-created")[:3]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return u"/blog/%d" % item.id

urlpatterns = patterns('blog.views',
    url(r'^$', PostIndexView.as_view(), name='index'),

    url(r'^(?P<pk>\d*)$', PostDetailView.as_view(), name="post"),

    url(r'^(?P<slug>[^/]+)/$', PostDetailView.as_view(), name="post"),


    url(r'^archives/$', ListView.as_view(
        queryset=Post.objects.all().order_by("-created"),
                                             template_name="archives.html")),

     url(r'^tag/(?P<tag>\w*)$', 'tagpage'),
     url(r'^feed/$', BlogFeed()),

)