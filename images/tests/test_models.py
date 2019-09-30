# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase, override_settings

from accounts.factories import UserFactory
from images.factories import ImageFactory
from images.models import Image

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class ImageModelTestCase(TestCase):
    """
    Tests the Image model.
    """
    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(ImageModelTestCase, self).tearDown()

    def test_if_no_title_uses_image_name(self):
        """
        If there's no title then the image's name should be the default.
        """
        with open(
            os.path.join(settings.BASE_DIR, 'images', 'tests', 'data', 'image.png'), "rb"
        ) as image_file:
            image = Image(
                image=SimpleUploadedFile("test.png", image_file.read())
            )
        image.set_title()
        self.assertEquals('test.png', image.title)

    @override_settings(DES_KEY='abcd1234')
    def test_can_created_encrypted_key(self):
        """
        Tests that the DES key encrypts properly
        """
        i = Image(pk=1)
        self.assertEquals('fQj1bFDkn3g', i.generate_encrypted_key())
        i.pk = 2
        self.assertEquals('i76tPgXaavF', i.generate_encrypted_key())

    @patch('images.models.Image.set_title')
    @patch('images.models.Image.generate_encrypted_key')
    def test_can_all_create_methods(self, generate_encrypted_key, set_title):
        """
        The encrypted key should be a created automatically.
        """
        ImageFactory.create()
        self.assertEquals(1, generate_encrypted_key.call_count)
        self.assertEquals(1, set_title.call_count)

    def test_image_knows_file_extension(self):
        """
        Tests an image knows its file extension.
        """
        image = ImageFactory.create()
        self.assertEquals(image.file_extension, 'png')

    def test_image_knows_mime_type(self):
        """
        Tests an image knows its file extension.
        """
        image = ImageFactory.create()
        self.assertEquals(image.mime_type, 'image/png')

    @override_settings(DES_KEY='abcd1234')
    def test_image_knows_raw_url(self):
        """
        Tests an image knows its file extension.
        """
        image = ImageFactory.create(pk=1)
        self.assertEquals(
            image.get_raw_url(),
            reverse('images:image_detail_raw', kwargs={'slug': image.encrypted_key, 'extension': image.file_extension})
        )

    def test_can_get_images_uploaded_by_a_user(self):
        """
        Tests that the manager can get images specifically uploaded by a user.
        """
        user_1 = UserFactory.create()
        user_2 = UserFactory.create()
        image_1a = ImageFactory.create(uploaded_by=user_1)
        image_1b = ImageFactory.create(uploaded_by=user_1)
        image_2a = ImageFactory.create(uploaded_by=user_2)
        self.assertEquals([image_1b, image_1a], list(Image.objects.filter_uploaded_by(user_1)))
        self.assertEquals([image_2a], list(Image.objects.filter_uploaded_by(user_2)))
