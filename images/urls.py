# -*- coding: utf-8 -*-
"""
URLs to manage accounts.
"""
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from images.views import ImageDetailView, ImageListView, mutli_image_upload, delete_image

urlpatterns = patterns(
    '',
    url(r'^upload/$', login_required(mutli_image_upload), name='upload'),
    url(r'^(?P<slug>[\d\w]+)/$', ImageDetailView.as_view(), name='image_detail'),
    url(r'^(?P<slug>[\d\w]+)/delete/$', delete_image, name='image_delete'),
    url(r'^$', login_required(ImageListView.as_view()), name='image_list'),
)
