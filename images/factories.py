# -*- coding: utf-8 -*-
"""
Factory for creating images.
"""
from __future__ import unicode_literals

import os

from django.core.files.uploadedfile import SimpleUploadedFile

from images.models import Image
from search.factories import SearchStubFactory

IMAGE_FILE = os.path.join(os.path.dirname(__file__), 'tests', 'data', 'image.png')


class ImageFactory(SearchStubFactory):
    """
    Factory for creating an image.
    """
    image = SimpleUploadedFile('image.png', open(IMAGE_FILE, 'rb').read(), 'image/png')

    class Meta(object):
        model = Image
