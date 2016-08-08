# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class SearchStubManager(models.Manager):
    """
    Manager for filtering Images.
    """
    def filter_uploaded_by(self, uploaded_by):
        """
        Filters images uploaded by a given user.
        :type uploaded_by: User
        """
        return self.filter(uploaded_by=uploaded_by)


class SearchStub(models.Model):
    """
    A proxy model that serves as a search stub.
    """
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True

    def get_autocomplete_thumbnail(self):
        """
        Override to provide a thumbnail to autocomplete.
        """
        raise NotImplementedError('You must implement an autocomplete thumbnail method')

    objects = SearchStubManager()
