# -*- coding: utf-8 -*-
"""
Factory for creating a test user.
"""
from __future__ import unicode_literals

import factory

from accounts.factories import UserFactory
from youtube.models import YoutubeVideo


class YoutubeVideoFactory(factory.DjangoModelFactory):
    """
    Factory for creating a test user
    """
    youtube_id = factory.Sequence(lambda n: "video-{}".format(n))
    uploaded_by = factory.SubFactory(UserFactory)

    class Meta(object):
        model = YoutubeVideo
