# -*- coding: utf-8 -*-
"""
Search indexes for the image app.
"""
from __future__ import unicode_literals

from haystack import indexes

from youtube.models import YoutubeVideo


class YoutubeVideoIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index for the Image model.
    """
    text = indexes.CharField(document=True, use_template=True)
    uploaded_by = indexes.CharField(model_attr='uploaded_by')
    date_created = indexes.DateTimeField(model_attr='date_created')
    date_modified = indexes.DateTimeField(model_attr='date_modified')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return YoutubeVideo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
