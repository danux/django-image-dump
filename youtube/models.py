# -*- coding: utf-8 -*-
"""
Models representing a Youtube video.
"""
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from pytube import YouTube

from search.models import SearchStub, SearchStubManager


class YoutubeVideoManager(SearchStubManager):
    """
    Manager for YoutubeVideo class.
    """
    def filter_downloaded(self):
        return self.filter(downloaded=True)


class YoutubeVideo(SearchStub):
    """
    Model representing a single Youtube video.
    """
    title = models.CharField(max_length=250, null=True)
    youtube_id = models.CharField(_('YouTube ID'), max_length=20, db_index=True, unique=True)
    file_path = models.CharField(max_length=250, null=True)
    downloaded = models.BooleanField(default=False)

    objects = YoutubeVideoManager()

    def download(self):
        """
        Downloads the YouTube video and sets the video's title.
        """
        yt = YouTube('https://www.youtube.com/watch?v={0}'.format(self.youtube_id))
        self.title = yt.title

        my_stream = yt.streams.first()
        self.file_path = '{0}.mp4'.format(self.youtube_id)
        my_stream.download(output_path=settings.YOUTUBE_DOWNLOAD_ROOT, filename=self.youtube_id)
        self.downloaded = True
        self.save()

    def get_absolute_url(self):
        return reverse('youtube:youtube_video_detail', kwargs={'youtube_id': self.youtube_id})

    def get_video_url(self):
        """
        Returns the URL of the downloaded video.
        """
        if self.file_path is not None:
            return os.path.join(settings.YOUTUBE_DOWNLOAD_URL, self.file_path)
        else:
            return ''

    def get_autocomplete_thumbnail(self):
        """
        Returns a thumbnail for auto search.
        """
        return '//img.youtube.com/vi/{0}/0.jpg'.format(self.youtube_id)
