from django.shortcuts import render_to_response
from blog.models import Post
from django.views.generic import DetailView, ListView
from taggit.models import Tag, TaggedItem
from django.db.models import Count

def tagpage(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render_to_response ("tagpage.html", {"posts":posts, "tag":tag})

def index(request):
    return render_to_response("blog.html", {"posts":posts})

class PostIndexView(ListView):
    template_name="blog.html"
    queryset=Post.objects.select_related().filter(postimage__is_cover=True).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super(PostIndexView, self).get_context_data(**kwargs)
        context['tags'] = TaggedItem.objects.filter(content_type__app_label='blog').values('tag__name').annotate(Count('tag__name'))
        return context

class PostDetailView(DetailView):
    template_name = 'post.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = context['object']
        body_len = len(post.body)
        half = int(body_len/2)
        context['body_half_len'] = half
        context['banner'] = post.postimage_set.filter(is_banner=True)
        context['images'] = post.postimage_set.filter(is_banner=False, is_video=False)
        context['tags'] = TaggedItem.objects.filter(content_type__app_label='blog').values('tag__name').annotate(Count('tag__name'))
        return context