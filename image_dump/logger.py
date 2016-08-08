# coding: utf-8
"""
Basic logging wrapper that pre-configures all log entries to have the IP address and user information.
"""
import logging

from structlog import get_logger, configure
from structlog.stdlib import LoggerFactory


class StructLogger(object):
    """
    Logging class.
    """
    @classmethod
    def get_logger(cls, logger_name, request=None):
        """
        Initialises the logger and attaches the mandatory information.

        :type logger_name: str | unicode
        :type request: django.http.HttpRequest
        """
        logging.basicConfig()
        configure(logger_factory=LoggerFactory())
        log = get_logger(logger_name)
        log.propagate = False
        if request is not None:
            log = log.bind(
                user=request.user.username or 'Anonymous User',
                user_agent=request.META.get('HTTP_USER_AGENT', 'UNKNOWN'),
                ip_address=request.META.get('REMOTE_ADDR', 'UNKNOWN'),
                path=request.path,
            )
        return log
