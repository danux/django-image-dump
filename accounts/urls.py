# -*- coding: utf-8 -*-
"""
URLs to manage accounts.
"""
from __future__ import unicode_literals
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'accounts/login.html'}
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': '/'}
    ),
)
