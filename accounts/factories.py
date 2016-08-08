# -*- coding: utf-8 -*-
"""
Factory for creating a test user.
"""
from __future__ import unicode_literals

import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    """
    Factory for creating a test user
    """
    first_name = factory.Sequence(lambda n: "First name {}".format(n))
    last_name = factory.Sequence(lambda n: "Last name {}".format(n))
    email = factory.Sequence(lambda n: "user{}@example.com".format(n))
    username = factory.Sequence(lambda n: "username{}".format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = False
    is_staff = False
    is_active = True

    class Meta(object):
        model = get_user_model()
