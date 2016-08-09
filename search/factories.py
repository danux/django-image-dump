# -*- coding: utf-8 -*-
"""
Factory providing a strub for
"""
from __future__ import unicode_literals

import factory

from accounts.factories import UserFactory


class SearchStubFactory(factory.DjangoModelFactory):
    """
    Factory for creating a test user
    """
    uploaded_by = factory.SubFactory(UserFactory)
