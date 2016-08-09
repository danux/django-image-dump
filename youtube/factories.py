# -*- coding: utf-8 -*-
"""
Factory for creating a test YoutubeVideo.
"""
from __future__ import unicode_literals

import factory

from search.factories import SearchStubFactory
from youtube.models import YoutubeVideo


class YoutubeVideoFactory(SearchStubFactory):
    """
    Factory for creating a test user
    """
    youtube_id = factory.Sequence(lambda n: "video-{}".format(n))

    class Meta(object):
        model = YoutubeVideo
