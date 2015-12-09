# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from haystack.generic_views import SearchView

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from accounts.factories import UserFactory
from images.models import Image


class ImageBrowsingTestCase(TestCase):
    """
    Tests images can be browsed.
    """
    def setUp(self):
        super(ImageBrowsingTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    def test_can_search_images(self):
        """
        Tests the images can be listed out
        """
        response = self.client.get(reverse('images:image_search'))
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], SearchView)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_must_be_logged_in_to_search(self):
        """
        Users must be logged in to browse images
        """
        self.client.logout()
        response = self.client.get(reverse('images:image_search'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('accounts:login'), reverse('images:image_search')))
