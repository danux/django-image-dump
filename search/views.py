# -*- coding: utf-8 -*-
"""
Views for the search module.
"""
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:10]
    if 'application/json' in request.META.get('HTTP_ACCEPT', []):
        content_type = 'application/json'
    else:
        content_type = 'text/plain'
    suggestions = [
        {
            'title': result.object.title,
            'thumbnail': result.object.get_autocomplete_thumbnail(),
            'url': result.object.get_absolute_url(),
        } for result in sqs
    ]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type=content_type)


class ImageSearchView(SearchView):
    """
    Custom search view to ensure users can only search their own images.
    """
    paginate_by = 12

    def get_queryset(self):
        queryset = super(ImageSearchView, self).get_queryset()
        return queryset.filter(uploaded_by=self.request.user)
