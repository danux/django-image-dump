# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase

from accounts.factories import UserFactory


class AccountIntegrationTestCase(TestCase):
    """
    Integration tests for the accounts package.
    """
    def test_login_page_loads(self):
        """
        Tests a user can login.
        """
        response = self.client.get(reverse('accounts:login'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_can_login_and_redirect(self):
        """
        Tests a user can login and be redirected back to the homepage.
        """
        user = UserFactory.create()
        response = self.client.post(
            reverse('accounts:login'),
            data={'username': user.username, 'password': 'password'},
            follow=True,
        )
        self.assertRedirects(response, reverse('images:upload'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_can_logout(self):
        """
        Tests the logout view.
        """
        user = UserFactory.create()
        self.client.login(**{'username': user.username, 'password': 'password'})
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('accounts:login'), reverse('images:upload')))
        self.assertFalse(response.context['user'].is_authenticated)
