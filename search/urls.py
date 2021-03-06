# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from search.views import ImageSearchView
from search.views import autocomplete


app_name = 'search'


urlpatterns = (
    url(r'^search/?$', login_required(ImageSearchView.as_view()), name='search'),
    url(r'^autocomplete/?$', login_required(autocomplete), name='autocomplete'),
)
