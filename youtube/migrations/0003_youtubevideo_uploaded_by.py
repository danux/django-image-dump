# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('youtube', '0002_auto_20160105_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='uploaded_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
