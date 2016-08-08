# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals

import requests
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from youtube.models import YoutubeVideo


class YoutubeVideoForm(forms.ModelForm):
    """
    Custom form for video downloads. Provides validation that the video exists on YouTube.
    """
    class Meta(object):
        model = YoutubeVideo
        fields = ['youtube_id']

    def clean_youtube_id(self):
        """
        Ensures the youtube_id is valid.
        """
        youtube_id = self.cleaned_data['youtube_id']
        test_url = 'https://www.googleapis.com/youtube/v3/videos?part=id&id={0}&key={1}'.format(
            youtube_id,
            settings.YOUTUBE_API_KEY
        )
        r = requests.get(test_url)
        if r.status_code != 200:
            raise forms.ValidationError(_('Could not read Youtube API.'))

        if r.json()['pageInfo']['totalResults'] == 0:
            raise forms.ValidationError(_('Unable to access a YouTube video with that ID. Please try again.'))
        else:
            return youtube_id
