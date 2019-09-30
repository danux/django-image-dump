# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView

from image_dump.logger import StructLogger
from youtube.forms import YoutubeVideoForm
from youtube.models import YoutubeVideo
from youtube.tasks import download_video


class YoutubeVideoCreateView(CreateView):
    """
    View for creating a new Youtube Video.
    """
    model = YoutubeVideo
    form_class = YoutubeVideoForm

    def __init__(self, **kwargs):
        super(YoutubeVideoCreateView, self).__init__(**kwargs)
        self.object = None

    def form_valid(self, form):
        """
        Saves the video, sets the uploaded by and downloads the video.

        :param form: The valid form
        :type form: YoutubeVideoForm
        """
        self.object = form.save(commit=False)
        self.object.uploaded_by = self.request.user
        self.object.save()
        download_video.delay(self.object)
        logger = StructLogger.get_logger(__name__, self.request)
        logger.info('Download successful', youtube_video_pk=self.object.pk, youtube_id=self.object.youtube_id)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Log invalid submissions.

        :param form: The invalid form
        :type form: YoutubeVideoForm
        """
        logger = StructLogger.get_logger(__name__, self.request)
        logger.error(
            msg='Download failed',
            youtube_id=self.request.POST.get('youtube_id', None),
            error=form.errors['youtube_id']
        )
        return super(YoutubeVideoCreateView, self).form_invalid(form)


class YoutubeVideoDetailView(DetailView):
    """
    View for looking at a video.
    """
    model = YoutubeVideo
    slug_url_kwarg = 'youtube_id'
    slug_field = 'youtube_id'

    def get_template_names(self):
        if self.get_object().downloaded:
            return super(YoutubeVideoDetailView, self).get_template_names()
        else:
            return 'youtube/youtubevideo_detail_pending.html'


class YoutubeVideoListView(ListView):
    """
    View for listing images
    """
    model = YoutubeVideo
    paginate_by = 12

    def get_queryset(self):
        """
        Limits query set to images uploaded by a given user.
        """
        return self.model.objects.filter_uploaded_by(self.request.user)
