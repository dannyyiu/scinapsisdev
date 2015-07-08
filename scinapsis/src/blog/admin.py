from django.contrib import admin
from django.db import models
from blog.models import Post
from blog.models import PostImage
from tinymce.widgets import TinyMCE

class InlineImage(admin.TabularInline):
    # Used for image uploading
    model = PostImage

class PostAdmin(admin.ModelAdmin):
    # Used for image uploading
    inlines = [InlineImage]
    formfield_overrides = {
    models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
}

#admin.site.register(Post)
admin.site.register(Post, PostAdmin)