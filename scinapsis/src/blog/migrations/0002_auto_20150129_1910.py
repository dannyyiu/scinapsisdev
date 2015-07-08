# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='abstract',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='execerpt',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postimage',
            name='is_banner',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postimage',
            name='is_cover',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postimage',
            name='is_video',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postimage',
            name='url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='meta',
            field=models.CharField(max_length=250, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
