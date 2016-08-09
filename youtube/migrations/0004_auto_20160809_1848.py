# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0003_youtubevideo_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_id',
            field=models.CharField(verbose_name='YouTube ID', max_length=20, unique=True, db_index=True),
        ),
    ]
