from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title  = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager ()
    
    def __unicode__(self):
        return self.title

class PostImage(models.Model):
    """ Used for admin image uploading. """
    post = models.ForeignKey(Post)
    image = models.ImageField()

    def to_str(self, image):
        return image.value_to_string