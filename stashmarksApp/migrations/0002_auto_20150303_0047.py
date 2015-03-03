# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('stashmarksApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('name', 'slug', 'owner')]),
        ),
    ]
