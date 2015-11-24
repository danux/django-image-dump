# Django Image Dump

[![Build Status](https://travis-ci.org/danux/django-image-dump.svg)](https://travis-ci.org/danux/django-image-dump)
[![Coverage Status](https://coveralls.io/repos/danux/django-image-dump/badge.svg?branch=master&service=github)](https://coveralls.io/github/danux/django-image-dump?branch=master)

This is an image upload app built on Django and using Blueimp's image uploader.

Whilst sites like imgur et al offer free image hosting their complex and often mis-understood terms and conditions mean
you can never be entirely sure who own your images.

I built this app to replace my scp workflow to move images to a random folder on a webserver for sharing.

Whilst very simple, it does boast some nice features.

## Features

- "Scaleable" slug generation - based on DES encryption of primary keys to prevent people guessing image URLs and ensuring uniqueness
- Drag n drop multi-image upload thanks to Blueimp
- Built on Bootstrap so it's _sort of_ responsive for easy to reskin
- Private image listings
- Proper image type detection through magic
- Open Graph integration so images share properly on compatible services
- Very easily adaptable to support other media types (namely changing the ``ALLOWED_MIME_TYPES`` setting)

## Disclaimer

This app was built for me. I run it on my own server for me. I've licensed it because it might be useful for someone else.

If you decide to use it please note only one user account is required to upload and have control over the app. If you plan to do something
with this I recommend finishing it off by adding some permissions and what not. I'll gladly pull back if you do.

Pay particular attention to ``DES_KEY = 'changeme'`` in ``app/settings.py`` - you need to change that a random 8 character string that only you know for the slug generator to be unique.


## CSRF Tokens

Whilst this uses the Blueimp uploader, some adjustments were made to make it work with Django CSRF protection. Just bare that in mind if you decide to do anything with this app.

I had to adjust Blueimp's ``ajaxSetup`` method to beforeSend a header with the CSRF Token.
