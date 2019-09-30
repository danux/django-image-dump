# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

import json

import magic
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView

from image_dump.logger import StructLogger
from images.models import Image


def multi_image_upload(request):
    """
    View for handling multi-image upload.

    :type request: HttpRequest
    """

    logger = StructLogger.get_logger(__name__, request)

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
            logger.error(msg='Upload failed', file_name=request.FILES['files[]'].name)
        else:
            image = Image.objects.create(image=request.FILES['files[]'], uploaded_by=request.user)
            thumbnail = image.make_thumbnail()
            response_dict = {'files': [{
                'name': image.title,
                'size': image.image.size,
                'url': image.get_absolute_url(),
                'thumbnailUrl': thumbnail,
                'deleteUrl': image.get_delete_url(),
                'deleteType': 'DELETE',
            }]}
            logger.info(
                msg='Upload successful',
                file_name=request.FILES['files[]'].name,
                image_pk=image.pk,
            )
        return JsonResponse(response_dict, content_type=content_type)
    else:
        return render(request=request, template_name='images/upload.html')


@csrf_protect
def delete_image(request, slug):
    """
    Deletes a specified image.
    :param request: The HTTP request
    :param slug: The Slug of the image
    """

    logger = StructLogger.get_logger(__name__, request)

    if request.method != 'DELETE':
        logger.error(msg='Delete failed', method=request.method)
        return HttpResponseNotAllowed(permitted_methods=['DELETE'])

    if not request.user.is_authenticated:
        logger.error(msg='User not authenticated')
        return HttpResponseForbidden()

    if 'application/json' in request.META.get('HTTP_ACCEPT', []):
        content_type = 'application/json'
    else:
        content_type = 'text/plain'
    image = get_object_or_404(Image, encrypted_key=slug)
    image.delete()
    logger.info(msg='Image deleted', image_pk=image.pk)
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


def latest_images(request):
    """
    Returns a JSON list of the latest images
    :param request: HttpRequest
    """
    if 'application/json' in request.META.get('HTTP_ACCEPT', []):
        content_type = 'application/json'
    else:
        content_type = 'text/plain'
    images = [
        {
            'title': image.title,
            'thumbnail': image.make_thumbnail('30'),
            'url': image.get_absolute_url(),
        } for image in Image.objects.filter_uploaded_by(request.user)[:10]
    ]
    the_data = json.dumps({
        'results': images
    })
    return HttpResponse(the_data, content_type=content_type)
