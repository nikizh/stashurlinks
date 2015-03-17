# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashmarksApp', '0002_auto_20150317_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='rating',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
