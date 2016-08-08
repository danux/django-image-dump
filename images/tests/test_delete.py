# -*- coding: utf-8 -*-
"""
Tests that images can be deleted.
"""
from __future__ import unicode_literals

import json

from django.test import TestCase

from accounts.factories import UserFactory
from images.factories import ImageFactory
from images.models import Image


class DeleteImageTestCase(TestCase):
    """
    Tests deleting an image.
    """
    def setUp(self):
        super(DeleteImageTestCase, self).setUp()
        user = UserFactory.create()
        self.client.login(**{'username': user.username, 'password': 'password'})
        self.image = ImageFactory()

    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(DeleteImageTestCase, self).tearDown()

    def test_can_delete(self):
        """
        Tests that sending a delete to the delete URL will delete the image.
        """
        response = self.client.delete(self.image.get_delete_url())
        expected_response_dict = {'files': {self.image.title: True}}
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_response_dict))
        self.assertRaises(Image.DoesNotExist, Image.objects.get, pk=self.image.pk)

    def test_must_be_logged_in_to_delete(self):
        """
        HTTP forbids guests.
        """
        self.client.logout()
        response = self.client.delete(self.image.get_delete_url())
        self.assertEquals(403, response.status_code)  # Proper 403, not a redirect to login

    def test_must_use_delete_method(self):
        """
        Only the DELETE method is allowed.
        """
        self.assertEquals(405, self.client.get(self.image.get_delete_url()).status_code)
        self.assertEquals(405, self.client.post(self.image.get_delete_url()).status_code)
        self.assertEquals(405, self.client.put(self.image.get_delete_url()).status_code)
