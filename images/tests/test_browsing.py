# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

import json

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

    @patch('search.models.SearchStubManager.filter_uploaded_by')
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


class LatestImagesTestCase(TestCase):
    """
    There must be a feed of the 10 latest images. This can be used by the autocomplete as the initial data.
    """
    def setUp(self):
        super(LatestImagesTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(LatestImagesTestCase, self).tearDown()

    @patch('images.models.Image.make_thumbnail')
    def test_can_get_latest_images(self, make_thumbnail):
        """
        Tests the list of latest images can be returned.
        :return:
        """
        make_thumbnail.return_value = 'thumbnail'
        ImageFactory.create(uploaded_by=self.user)
        image_1 = ImageFactory.create(uploaded_by=self.user)
        image_2 = ImageFactory.create(uploaded_by=self.user)
        image_3 = ImageFactory.create(uploaded_by=self.user)
        image_4 = ImageFactory.create(uploaded_by=self.user)
        image_5 = ImageFactory.create(uploaded_by=self.user)
        image_6 = ImageFactory.create(uploaded_by=self.user)
        image_7 = ImageFactory.create(uploaded_by=self.user)
        image_8 = ImageFactory.create(uploaded_by=self.user)
        image_9 = ImageFactory.create(uploaded_by=self.user)
        image_10 = ImageFactory.create(uploaded_by=self.user)
        response = self.client.get(reverse('images:latest_images'))
        expected_response_dict = {
            'results': [
                {'title': image_10.title, 'thumbnail': 'thumbnail', 'url': image_10.get_absolute_url()},
                {'title': image_9.title, 'thumbnail': 'thumbnail', 'url': image_9.get_absolute_url()},
                {'title': image_8.title, 'thumbnail': 'thumbnail', 'url': image_8.get_absolute_url()},
                {'title': image_7.title, 'thumbnail': 'thumbnail', 'url': image_7.get_absolute_url()},
                {'title': image_6.title, 'thumbnail': 'thumbnail', 'url': image_6.get_absolute_url()},
                {'title': image_5.title, 'thumbnail': 'thumbnail', 'url': image_5.get_absolute_url()},
                {'title': image_4.title, 'thumbnail': 'thumbnail', 'url': image_4.get_absolute_url()},
                {'title': image_3.title, 'thumbnail': 'thumbnail', 'url': image_3.get_absolute_url()},
                {'title': image_2.title, 'thumbnail': 'thumbnail', 'url': image_2.get_absolute_url()},
                {'title': image_1.title, 'thumbnail': 'thumbnail', 'url': image_1.get_absolute_url()},
            ]
        }
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_response_dict))
