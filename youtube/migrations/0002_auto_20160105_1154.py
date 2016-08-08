# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 1, 5, 11, 54, 9, 206381, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youtubevideo',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 5, 11, 54, 11, 278388, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
