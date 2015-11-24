# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
import json
import os
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from accounts.factories import UserFactory
from images.models import Image


class ImageUploadTestCase(TestCase):
    """
    Tests uploading an image.
    """
    def setUp(self):
        super(ImageUploadTestCase, self).setUp()
        user = UserFactory.create()
        self.client.login(**{'username': user.username, 'password': 'password'})

    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(ImageUploadTestCase, self).tearDown()

    def test_upload_page_renders(self):
        """
        Tests the upload form renders.
        """
        response = self.client.get(reverse('images:upload'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'images/upload.html')

    def test_homepage_redirects(self):
        """
        The homepage should redirect to the upload form.
        """
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('images:upload'))

    def test_user_must_be_logged_in(self):
        """
        Guests should have to login.
        """
        self.client.logout()
        response = self.client.get(reverse('images:upload'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('accounts:login'), reverse('images:upload')))

    @override_settings(ALLOWED_MIME_TYPES=[b'image/png'])
    @patch('images.models.Image.make_thumbnail')
    def test_uploading_returns_confirmation_json(self, make_thumbnail):
        """
        Once an image is uploaded a JSON response should be returned.
        """
        make_thumbnail.return_value = Mock()
        make_thumbnail.return_value.url = ''
        with open(
            os.path.join(settings.BASE_DIR, 'images', 'tests', 'data', 'image.png'), "rb"
        ) as image_file:
            image = SimpleUploadedFile("test.png", image_file.read(), content_type='image/png')
            response = self.client.post(reverse('images:upload'), data={'files[]': image}, follow=True)
        latest_image = Image.objects.latest('date_created')
        expected_response_dict = {'files': [{
            'name': latest_image.title,
            'size': latest_image.image.size,
            'url': latest_image.get_absolute_url(),
            'thumbnailUrl': '',
            'deleteUrl': latest_image.get_delete_url(),
            'deleteType': 'DELETE',
        }]}
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_response_dict))

    @override_settings(ALLOWED_MIME_TYPES=[b'image/jpeg'])
    def test_error_handling_mime_type(self):
        """
        If the image's mime type is not allowed  mime types list then an error should be returned.
        """
        with open(
            os.path.join(settings.BASE_DIR, 'images', 'tests', 'data', 'image.png'), "rb"
        ) as image_file:
            image = SimpleUploadedFile("test.png", image_file.read(), content_type='image/png')
            response = self.client.post(reverse('images:upload'), data={'files[]': image}, follow=True)
        expected_response_dict = {'files': [{
            'name': 'test.png',
            'size': 3847,
            'error': 'test.png is not a valid image file',
        }]}
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_response_dict))
