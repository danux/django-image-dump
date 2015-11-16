# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.forms import ImageField
from django.test import TestCase
from django.views.generic import CreateView
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
        self.assertIsInstance(response.context['view'], CreateView)
        self.assertTemplateUsed(response, 'images/upload.html')
        self.assertEquals(len(response.context['form'].fields), 1)
        self.assertIsInstance(response.context['form'].fields['image'], ImageField)

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

    def test_uploading_redirects_to_view_image(self):
        """
        Once an image is uploaded the user should be redirected to the image.
        """
        with open(
            os.path.join(settings.BASE_DIR, 'images', 'tests', 'data', 'image.png'), "rb"
        ) as image_file:
            image = SimpleUploadedFile("test.png", image_file.read(), content_type='image/png')
            response = self.client.post(reverse('images:upload'), data={'image': image}, follow=True)
        latest_image = Image.objects.latest('date_created')
        self.assertRedirects(response, latest_image.get_absolute_url())
