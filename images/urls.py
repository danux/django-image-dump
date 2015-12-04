# -*- coding: utf-8 -*-
"""
URLs to manage accounts.
"""
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from images.views import ImageDetailView, ImageListView, mutli_image_upload, delete_image, image_detail_raw


urlpatterns = patterns(
    '',
    url(r'^upload/$', login_required(mutli_image_upload), name='upload'),
    url(r'^list/$', login_required(ImageListView.as_view()), name='image_list'),
    url(r'^(?P<slug>[\d\w]+)/$', ImageDetailView.as_view(), name='image_detail'),
    url(r'^(?P<slug>[\d\w]+).(?P<extension>[\w]{3})$', image_detail_raw, name='image_detail_raw'),
    url(r'^(?P<slug>[\d\w]+)/delete/$', delete_image, name='image_delete'),
    url(r'^$', RedirectView.as_view(pattern_name='images:upload', permanent=False), name='index')
)
