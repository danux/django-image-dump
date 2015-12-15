# -*- coding: utf-8 -*-
"""
Tests the inline edit functionality is integrated.
"""
from __future__ import unicode_literals
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django_factory_boy.auth import UserFactory
from images.factories import ImageFactory
from images.models import Image
from images.perms import UploadedByEditInline


class PermissionTestCase(TestCase):
    """
    Tests that the permission is correct.
    """
    def tearDown(self):
        for image in Image.objects.all():
            image.delete()
        super(PermissionTestCase, self).tearDown()

    def test_returns_true_for_uploaded(self):
        """
        If the user uploaded the image it should return true.
        """
        image = ImageFactory.create()
        adaptor_field = MagicMock()
        adaptor_field.obj = image
        adaptor_field.request.user = image.uploaded_by
        self.assertTrue(UploadedByEditInline.can_edit(adaptor_field))

    def test_returns_false_for_other_users(self):
        image = ImageFactory.create()
        adaptor_field = MagicMock()
        adaptor_field.obj = image
        adaptor_field.request.user = UserFactory.create()
        self.assertFalse(UploadedByEditInline.can_edit(adaptor_field))

    def test_returns_false_for_anonymous_users(self):
        image = ImageFactory.create()
        adaptor_field = MagicMock()
        adaptor_field.obj = image
        adaptor_field.request.user = AnonymousUser()
        self.assertFalse(UploadedByEditInline.can_edit(adaptor_field))
