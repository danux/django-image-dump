# -*- coding: utf-8 -*-
"""
Provides a celery task for delayed saving to the database.
"""
from __future__ import absolute_import

from celery import shared_task

from image_dump.logger import StructLogger


@shared_task
def download_video(instance):
    """
    Task for downloading a video from YouTube.
    :param instance: YoutubeVideo
    """
    instance.download()
    logger = StructLogger.get_logger(__name__)
    logger.info(msg='Download complete', video_id=instance.pk, youtube_id=instance.youtube_id)
