# -*- coding: utf-8 -*-
"""
URLs to manage accounts.
"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView


app_name = 'accounts'


urlpatterns = (
    url(
        r'^login/$',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(next_page='/'),
        name='logout',
    ),
    url(
        '^change-password/$',
        PasswordChangeView.as_view(
            template_name='accounts/change-password.html',
            success_url='accounts:change_password_done',
        ),
        name='change_password',
    ),
    url(
        '^change-password/done/$',
        PasswordChangeDoneView.as_view(template_name='accounts/change-password-done.html'),
        name='change_password_done',
    )
)
