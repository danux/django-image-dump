# -*- coding: utf-8 -*-
"""
Permissions used for the inline edit plugin.
"""
from __future__ import unicode_literals


class UploadedByEditInline(object):

    @classmethod
    def can_edit(cls, adaptor_field):
        """
        If the user uploaded the instance of the class they can edit it.
        """
        if adaptor_field.obj.uploaded_by == adaptor_field.request.user:
            return True
        return False
