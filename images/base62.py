# -*- coding: utf-8 -*-
"""
Base 62 encoding. Chose to do this recursively for fun and to see if it could be done.
"""
from __future__ import unicode_literals
from string import ascii_lowercase, ascii_uppercase, digits


def base62encode(number):
    """
    Base 62 encoded integers.
    """
    try:
        number = int(number)
    except ValueError:
        raise ValueError('You must provide a non-negative integer for base62 encoding.')
    else:
        if number < 0:
            raise ValueError('You must provide a non-negative integer for base62 encoding.')

    alphabet = ascii_lowercase + ascii_uppercase + digits
    if number < len(alphabet):
        # Special case to skip recursion if we don't need it.
        return alphabet[number]

    def the_loop(base62, remainder):
        """
        Builds up the base62 encoding until the remainder hits 0.
        """
        new_remainder, pos = divmod(remainder, len(alphabet))
        if remainder < 1:
            return base62
        return the_loop(alphabet[pos] + base62, new_remainder)
    return the_loop('', number)
