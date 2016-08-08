# coding: utf-8
"""
Registers npower_auth app models with Django admin.
"""
from django.contrib import admin

from youtube.models import YoutubeVideo


admin.site.register(YoutubeVideo, admin.ModelAdmin)
