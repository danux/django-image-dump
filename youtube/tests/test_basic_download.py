# -*- coding: utf-8 -*-
"""
Tests basic download functionality.
"""
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.forms import CharField
from django.test import TestCase, override_settings
from django.views.generic import CreateView
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from accounts.factories import UserFactory
from youtube.forms import YoutubeVideoForm
from youtube.models import YoutubeVideo


class DownloadTestCase(TestCase):
    """
    Tests that videos are downloaded a
    """

    def setUp(self):
        super(DownloadTestCase, self).setUp()
        self.user = UserFactory.create()
        self.client.login(**{'username': self.user.username, 'password': 'password'})

    @override_settings(YOUTUBE_DOWNLOAD_ROOT='/youtube-downloads/')
    def test_can_download_and_set_title(self):
        """
        It should be possible to download a video and have the title automatically set.
        """

        class MockVideo(MagicMock):
            filename = 'Test Title'

        video = YoutubeVideo(youtube_id='_IMlaimDzTg')
        with patch('youtube.models.YouTube.filter') as mock_filter:
            with patch('youtube.models.YouTube.set_filename') as mock_set_filename:
                videos = [MockVideo(), MockVideo(), MockVideo()]
                mock_filter.return_value = videos
                video.uploaded_by = self.user
                video.download()
                mock_filter.assert_called_once_with('mp4')
                mock_set_filename.assert_called_once_with('_IMlaimDzTg')
                videos[-1].download.assert_called_once_with('/youtube-downloads/')

        self.assertEquals(video.title, 'Test Title')
        self.assertEquals(video.file_path, '_IMlaimDzTg.mp4')
        self.assertTrue(video.downloaded)

    def test_view_to_download_renders(self):
        """
        Tests the view for downloading Youtube.
        """
        response = self.client.get(reverse('youtube:youtube_video_create'))
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['view'], CreateView)
        self.assertEquals(1, len(response.context['form'].fields))
        self.assertIsInstance(response.context['form'].fields['youtube_id'], CharField)

    def test_user_must_be_logged_in(self):
        """
        Guests should have to login.
        """
        self.client.logout()
        response = self.client.get(reverse('youtube:youtube_video_create'))
        self.assertRedirects(
            response,
            '{0}?next={1}'.format(reverse('accounts:login'), reverse('youtube:youtube_video_create'))
        )

    @patch('youtube.models.YoutubeVideo.get_video_url')
    @patch('youtube.forms.YoutubeVideoForm.clean_youtube_id')
    def test_creating_downloads_video(self, patched_clean_youtube_id, patched_get_video_url):
        """
        Creating a Youtube Video downloads the video.
        """
        patched_get_video_url.return_value = '/video.mp4'
        patched_clean_youtube_id.return_value = '_IMlaimDzTg'
        with patch('youtube.tasks.download_video.delay') as patched_download_delay:
            response = self.client.post(reverse('youtube:youtube_video_create'), data={'youtube_id': '_IMlaimDzTg'})
            self.assertEquals(patched_download_delay.call_count, 1)
        self.assertRedirects(response, reverse('youtube:youtube_video_detail', kwargs={'youtube_id': '_IMlaimDzTg'}))

    @patch('requests.get')
    def test_checks_youtube_must_return_200(self, patched_head):
        """
        Tests that the Youtube ID is tested.
        """
        patched_head.return_value.status_code = 404
        data = {'youtube_id': '_IMlaimDzTg'}
        form = YoutubeVideoForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['youtube_id'], ['Could not read Youtube API.'])

    @patch('requests.get')
    def test_checks_valid_youtube_id(self, patched_head):
        """
        Tests that the Youtube ID is tested.
        """
        patched_head.return_value.status_code = 200
        patched_head.return_value.json.return_value = {'pageInfo': {'totalResults': 0}}
        data = {'youtube_id': '_IMlaimDzTg'}
        form = YoutubeVideoForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['youtube_id'],
            ['Unable to access a YouTube video with that ID. Please try again.']
        )
