# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.views.generic import ListView, DetailView
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from accounts.factories import UserFactory
from images.factories import ImageFactory
from images.models import Image


class ImageBrowsingTestCase(TestCase):
    """
    Tests images can be browsed.
    """
    def setUp(self):
        super(ImageBrowsingTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(ImageBrowsingTestCase, self).tearDown()

    @patch('images.models.ImageManager.filter_uploaded_by')
    def test_can_list_images(self, filter_uploaded_by):
        """
        Tests the images can be listed out
        """
        filter_uploaded_by.return_value = Image.objects.all()
        response = self.client.get(reverse('images:image_list'))
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], ListView)
        self.assertTemplateUsed(response, 'images/image_list.html')
        filter_uploaded_by.assert_called_once_with(self.user)

    def test_must_be_logged_in_to_list(self):
        """
        Users must be logged in to browse images
        """
        self.client.logout()
        response = self.client.get(reverse('images:image_list'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('accounts:login'), reverse('images:image_list')))

    def test_can_view_image(self):
        """
        Tests an existing image can be viewed.
        """
        image = ImageFactory.create()
        response = self.client.get(image.get_absolute_url())
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], DetailView)
        self.assertTemplateUsed(response, 'images/image_detail.html')

    def test_can_view_raw_image(self):
        """
        If the image is requested with a file extension the raw image is sent.
        """
        image = ImageFactory.create()
        response = self.client.get(image.get_raw_url())
        self.assertEquals(response.get('content-type'), 'image/png')
