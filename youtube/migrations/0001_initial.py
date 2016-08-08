# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('youtube_id', models.CharField(max_length=20, db_index=True, unique=True)),
                ('title', models.CharField(max_length=250, null=True)),
                ('file_path', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]
