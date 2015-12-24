# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from Crypto.Cipher import DES
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from images.base62 import base62encode
from sorl.thumbnail import get_thumbnail
import magic
import struct


class ImageManager(models.Manager):
    """
    Manager for filtering Images.
    """
    def filter_uploaded_by(self, uploaded_by):
        """
        Filters images uploaded by a given user.
        :type uploaded_by: User
        """
        return self.filter(uploaded_by=uploaded_by)


class Image(models.Model):
    """
    Model representing an image that has been uploaded to the system.
    """
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='u/%Y/%m/')
    encrypted_key = models.CharField(max_length=250, db_index=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = ImageManager()

    def get_absolute_url(self):
        """
        The URL for viewing the image.
        """
        return reverse('images:image_detail', kwargs={'slug': self.encrypted_key})

    def get_raw_url(self):
        """
        The URL for viewing the raw image.
        """
        return reverse('images:image_detail_raw', kwargs={'slug': self.encrypted_key, 'extension': self.file_extension})

    def get_delete_url(self):
        """
        Returns the URL to delete the image
        """
        return reverse('images:image_delete', kwargs={'slug': self.encrypted_key})

    def generate_encrypted_key(self):
        """
        Generates a DES encrypted version of the primary key then wraps it in base 64.
        """
        d = DES.new(settings.DES_KEY)
        self.encrypted_key = base62encode(struct.unpack(str('<Q'), d.encrypt(
            struct.pack(str('<Q'), self.pk)
        ))[0])
        return self.encrypted_key

    def set_title(self):
        """
        Sets the title to the name of the file.
        """
        if self.title == '' or self.title is None:
            self.title = self.image.file.name.split('/')[-1]

    def make_thumbnail(self, dimension=80):
        """
        Makes a thumbnail of the image.

        :type dimension: str | unicode
        """
        try:
            if self.image.height > self.image.width:
                thumbnail = get_thumbnail(self.image, 'x{0}'.format(int(dimension)), quality=99).url
            else:
                thumbnail = get_thumbnail(self.image, str(dimension), quality=99).url
        except IOError:
            thumbnail = ''
        return thumbnail

    @property
    def file_extension(self):
        """
        Returns the image's file extension.
        """
        return self.image.file.name.split('.')[-1]

    @property
    def mime_type(self):
        """
        Returns the image's mime type, using magic.
        """
        return magic.from_file(self.image.file.name, mime=True)

    class Meta(object):
        ordering = ['-date_created']


def post_create_setup(sender, **kwargs):
    """
    If an image is being created then generate the unique key and set the title.

    :type sender: models.Model
    """
    del sender  # not used
    if kwargs['created']:
        instance = kwargs['instance']
        instance.generate_encrypted_key()
        instance.set_title()
        instance.save()
post_save.connect(post_create_setup, sender=Image)
