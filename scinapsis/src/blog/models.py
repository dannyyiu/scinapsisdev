from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title  = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, blank=True)
    pinned = models.BooleanField(default=False)

    abstract = models.TextField(blank=True)
    body = models.TextField()
    execerpt = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    meta = models.CharField(max_length=250, blank=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # if slug is empty, use the title
            from django.template.defaultfilters import slugify
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    """ Used for admin image uploading. """
    post = models.ForeignKey(Post)
    image = models.ImageField(blank=True)
    url = models.URLField(default='',blank=True)
    is_banner = models.BooleanField(default=False)
    is_cover = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

    def to_str(self, image):
        return image.value_to_string

class Comment(models.Model):
    ## tentative model for comments
    name = models.TextField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    ip_addr = models.GenericIPAddressField()