# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from images.models import Image
import magic
import json


def multi_image_upload(request):
    """
    View for handling multi-image upload.

    :type request: HttpRequest
    """
    if request.method == 'POST':
        if 'application/json' in request.META.get('HTTP_ACCEPT', []):
            content_type = 'application/json'
        else:
            content_type = 'text/plain'

        # TODO: See if there's a safer way to inspect file than .read() - .chunks() isn't accepted by magic.
        mime_type = magic.from_buffer(request.FILES['files[]'].read(), mime=True)
        if mime_type not in settings.ALLOWED_MIME_TYPES:
            response_dict = {'files': [{
                'name': request.FILES['files[]'].name,
                'size': request.FILES['files[]'].size,
                'error': _('{} is not a valid image file').format(request.FILES['files[]'].name),
            }]}
        else:
            image = Image.objects.create(image=request.FILES['files[]'], uploaded_by=request.user)
            thumbnail = image.make_thumbnail()
            response_dict = {'files': [{
                'name': image.title,
                'size': image.image.size,
                'url': image.get_absolute_url(),
                'thumbnailUrl': thumbnail.url,
                'deleteUrl': image.get_delete_url(),
                'deleteType': 'DELETE',
            }]}
        return JsonResponse(response_dict, content_type=content_type)
    else:
        return render_to_response('images/upload.html', context_instance=RequestContext(request))


@csrf_protect
def delete_image(request, slug):
    """
    Deletes a specified image.
    :param request: The HTTP request
    :param slug: The Slug of the image
    """
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(permitted_methods=['DELETE'])

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if 'application/json' in request.META.get('HTTP_ACCEPT', []):
        content_type = 'application/json'
    else:
        content_type = 'text/plain'
    image = get_object_or_404(Image, encrypted_key=slug)
    image.delete()
    response_dict = {
        'files': {image.title: True}
    }
    return JsonResponse(response_dict, content_type=content_type)


class ImageDetailView(DetailView):
    """
    View for displaying a single image
    """
    slug_field = 'encrypted_key'
    model = Image


class ImageListView(ListView):
    """
    View for listing images
    """
    model = Image
    paginate_by = 12

    def get_queryset(self):
        """
        Limits query set to images uploaded by a given user.
        """
        return self.model.objects.filter_uploaded_by(self.request.user)


def image_detail_raw(request, slug, extension):
    """
    View for displaying a single image

    :type request: HttpRequest
    :type slug: str | unicode
    :type extension: str | unicode

    :returns HttpResponse
    """
    del extension  # Not actually required.
    the_object = get_object_or_404(Image, encrypted_key=slug)
    image_data = open(the_object.image.file.name, "rb").read()
    return HttpResponse(image_data, content_type=the_object.mime_type)


class ImageSearchView(SearchView):
    """
    Custom search view to ensure users can only search their own images.
    """
    paginate_by = 12

    def get_queryset(self):
        queryset = super(ImageSearchView, self).get_queryset()
        return queryset.filter(uploaded_by=self.request.user)


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:10]
    suggestions = [
        {
            'title': result.object.title,
            'thumbnail': result.object.make_thumbnail('30').url,
            'url': result.object.get_absolute_url(),
        } for result in sqs
    ]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
