# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashmarksApp', '0003_ratings_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='rating',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='ratings',
            old_name='rating',
            new_name='liked',
        ),
    ]
