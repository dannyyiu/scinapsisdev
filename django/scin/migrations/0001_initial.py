# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pub_figure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('figure_id', models.IntegerField()),
                ('header', models.CharField(max_length=800)),
                ('content', models.TextField()),
                ('url', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pub_material_n_method',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_id', models.IntegerField()),
                ('header', models.CharField(max_length=800)),
                ('content_seq', models.IntegerField()),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pub_meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_id', models.CharField(max_length=50)),
                ('src_address', models.CharField(max_length=100)),
                ('pdf_address', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=800)),
                ('editors', models.CharField(max_length=200)),
                ('pub_date', models.DateField()),
                ('copyright', models.TextField()),
                ('data_availibility', models.TextField()),
                ('funding', models.TextField()),
                ('competing_interest', models.TextField()),
                ('rec_update_time', models.DateTimeField(auto_now=True)),
                ('rec_update_by', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pub_material_n_method',
            name='doc_id',
            field=models.ForeignKey(to='scin.pub_meta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pub_figure',
            name='doc_id',
            field=models.ForeignKey(to='scin.pub_meta'),
            preserve_default=True,
        ),
    ]
