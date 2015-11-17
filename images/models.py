# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
from string import ascii_lowercase, ascii_uppercase, digits
import struct
from Crypto.Cipher import DES
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from sorl.thumbnail import get_thumbnail


class Image(models.Model):
    """
    Model representing an image that has been uploaded to the system.
    """
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='u/%Y/%m/')
    encrypted_key = models.CharField(max_length=250, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """
        The URL for viewing the image.
        """
        return reverse('images:image_detail', kwargs={'slug': self.encrypted_key})

    def get_delete_url(self):
        """
        Returns the URL to delete the image
        """
        return reverse('images:image_delete', kwargs={'slug': self.encrypted_key})

    def generate_encrypted_key(self):
        """
        Generates a DES encrypted version of the primary key then wraps it in base 64.
        """
        def base62encode(number):
            """
            Base 62 encoded integers.
            """
            alphabet = ascii_lowercase + ascii_uppercase + digits
            base62 = ''
            while number:
                number, i = divmod(number, len(alphabet))
                base62 = alphabet[i] + base62
            return base62 or alphabet[0]

        d = DES.new(settings.DES_KEY)
        self.encrypted_key = base62encode(struct.unpack(str('<Q'), d.encrypt(
            struct.pack(str('<Q'), self.pk)
        ))[0])

    def make_thumbnail(self):
        """
        Makes a thumbnail of the image.
        """
        if self.image.height > self.image.width:
            thumbnail = get_thumbnail(self.image, 'x80', quality=99)
        else:
            thumbnail = get_thumbnail(self.image, '80', quality=99)
        return thumbnail


def generate_encrypted_key(sender, **kwargs):
    """
    If an image is being created then generate the unique key.
    """
    if kwargs['created']:
        instance = kwargs['instance']
        instance.generate_encrypted_key()
        if instance.title == '' or instance.title is None:
            instance.title = instance.image.file.name.split('/')[-1]
        instance.save()
post_save.connect(generate_encrypted_key, sender=Image)
