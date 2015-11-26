# -*- coding: utf-8 -*-
"""
Tests for my own recurive
"""
from __future__ import unicode_literals
from django.test import TestCase
from images.base62 import base62encode


class Base62TestCase(TestCase):
    """
    Tests a few base62 values.
    """
    def test_basic_values(self):
        """
        Expected outcomes checked against: https://rot47.net/base.html
        """
        self.assertEquals(base62encode(0), 'a')
        self.assertEquals(base62encode(1), 'b')
        self.assertEquals(base62encode(61), '9')
        self.assertEquals(base62encode(62), 'ba')
        self.assertEquals(base62encode(63), 'bb')

    def test_must_be_positive(self):
        """
        Tests numbers must be positive
        """
        self.assertRaises(ValueError, base62encode, -10)
        self.assertRaises(ValueError, base62encode, -100)

    def test_must_be_integer(self):
        """
        Value error if the value is not an int.
        """
        self.assertRaises(ValueError, base62encode, 'string')
        self.assertRaises(ValueError, base62encode, b'bytes')

    def test_floats_are_truncated(self):
        """
        Just in case...
        """
        self.assertEquals(base62encode(1.2), 'b')
