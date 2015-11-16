# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
import magic
from images.models import Image


def mutli_image_upload(request):
    """
    View for handling multi-image upload.
    """
    if request.method == 'POST':
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            content_type = 'application/json'
        else:
            content_type = 'text/plain'

        # TODO: See if there's a safer way to inspect file than .read() - .chunks() isn't accepted by magic.
        mime_type = magic.from_buffer(request.FILES['files[]'].read(), mime=True)
        if mime_type not in settings.ALLOWED_MIME_TYPES:
            response_dict = dict(files=[dict(
                name=request.FILES['files[]'].name,
                size=request.FILES['files[]'].size,
                error='{0} is not a valid image file'.format(request.FILES['files[]'].name)
            )])
        else:
            image = Image.objects.create(image=request.FILES['files[]'])
            thumbnail = image.make_thumbnail()
            response_dict = dict(files=[dict(
                name=image.title,
                size=image.image.size,
                url=image.get_absolute_url(),
                thumbnailUrl=thumbnail.url,
                deleteUrl=image.get_delete_url(),
                deleteType='DELETE',
            )])
        return JsonResponse(response_dict, **{'content_type': content_type})
    else:
        return render_to_response('images/upload.html', context_instance=RequestContext(request))


@csrf_protect
def delete_image(request, slug):
    """
    Deletes a specified image.
    """
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(permitted_methods=['DELETE'])

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        content_type = 'application/json'
    else:
        content_type = 'text/plain'
    image = get_object_or_404(Image, encrypted_key=slug)
    image.delete()
    response_dict = {
        'files': {image.title: True}
    }
    return JsonResponse(response_dict, **{'content_type': content_type})


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
