# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    def slug_new_val(apps, schema_editor):
        Post = apps.get_model('blog','post')
        for post in Post.objects.all():
            if not post.slug:
                # if slug is empty, use the title
                from django.template.defaultfilters import slugify
                post.slug = slugify(post.title)
                post.save()

            imgs = post.postimage_set.all()
            if imgs:
                imgs[0].is_cover=True
                imgs[0].save()

    dependencies = [
        ('blog', '0002_auto_20150129_1910'),
    ]

    operations = [
        migrations.RunPython(slug_new_val)
    ]
