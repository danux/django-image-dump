# -*- coding: utf-8 -*-
"""
Provides a celery task for delayed saving to the database.
"""
from __future__ import absolute_import

from celery import shared_task
from haystack.management.commands import update_index

from image_dump.logger import StructLogger


@shared_task
def rebuild_index():
    """
    Task for downloading a video from YouTube.
    :param instance: YoutubeVideo
    """
    update_index.Command().handle(interactive=False)
    logger = StructLogger.get_logger(__name__)
    logger.info(msg='Re-indexed search')
