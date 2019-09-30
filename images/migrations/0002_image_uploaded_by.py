# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
