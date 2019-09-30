# -*- coding: utf-8 -*-
"""
Search integration tests
"""
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase
from haystack.generic_views import SearchView

from accounts.factories import UserFactory


class SearchTestCase(TestCase):
    """
    Tests images can be searched.
    """
    def setUp(self):
        super(SearchTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    def test_can_search(self):
        """
        Tests the images can be listed out
        """
        response = self.client.get(reverse('search:search'))
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], SearchView)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_must_be_logged_in_to_search(self):
        """
        Users must be logged in to browse images
        """
        self.client.logout()
        response = self.client.get(reverse('search:search'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('accounts:login'), reverse('search:search')))
