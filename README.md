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
- Set image titles with in-line editing
- Built on Bootstrap so it's _sort of_ responsive for easy skinning
- Private image listings and support for a search engine (through Haystack) with autocomplete using Twitter's typeahead
- Proper image type detection through magic
- Open Graph integration so images share properly on compatible services
- Very easily adaptable to support other media types (namely changing the ``ALLOWED_MIME_TYPES`` setting)


## Disclaimer

This app was built for me. I run it on my own server for me. I've licensed it because it might be useful for someone else.

If you decide to use this app please bare in mind it's only really been tested for one person. Other people's images shouldn't show up
in search results or autocomplete, but it's possible I've overlooked this as I don't really test it.

Pay particular attention to ``DES_KEY = 'changeme'`` in ``app/settings.py`` - you need to change that a random 8 character string that only you know for the slug generator to be unique.


## CSRF Tokens

Whilst this uses the Blueimp uploader, some adjustments were made to make it work with Django CSRF protection. Just bare that in mind if you decide to do anything with this app.

I had to adjust Blueimp's ``ajaxSetup`` method to beforeSend a header with the CSRF Token.
