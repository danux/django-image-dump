# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from youtube.views import YoutubeVideoCreateView, YoutubeVideoDetailView, YoutubeVideoListView


app_name = 'youtube'


urlpatterns = (
    url(r'^save/$', login_required(YoutubeVideoCreateView.as_view()), name='youtube_video_create'),
    url(r'^list/$', login_required(YoutubeVideoListView.as_view()), name='youtube_video_list'),
    url(r'^(?P<youtube_id>[-_\d\w]+)/$', YoutubeVideoDetailView.as_view(), name='youtube_video_detail'),
)
