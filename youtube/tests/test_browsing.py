# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.views.generic import ListView

from youtube.models import YoutubeVideo

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from accounts.factories import UserFactory


class YoutubeVideoBrowsingTestCase(TestCase):
    """
    Tests images can be browsed.
    """
    def setUp(self):
        super(YoutubeVideoBrowsingTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    @patch('search.models.SearchStubManager.filter_uploaded_by')
    def test_can_list_images(self, filter_uploaded_by):
        """
        Tests the images can be listed out
        """
        filter_uploaded_by.return_value = YoutubeVideo.objects.all()
        response = self.client.get(reverse('youtube:youtube_video_list'))
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], ListView)
        self.assertTemplateUsed(response, 'youtube/youtubevideo_list.html')
        filter_uploaded_by.assert_called_once_with(self.user)

    def test_must_be_logged_in_to_list(self):
        """
        Users must be logged in to browse images
        """
        self.client.logout()
        response = self.client.get(reverse('youtube:youtube_video_list'))
        self.assertRedirects(
            response,
            '{0}?next={1}'.format(reverse('accounts:login'), reverse('youtube:youtube_video_list'))
        )
