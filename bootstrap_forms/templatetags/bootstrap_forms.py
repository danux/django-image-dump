# -*- coding: utf-8 -*-
"""
Template filters to workout which classes to add.
"""
from django import template


register = template.Library()


@register.filter
def apply_form_controls(field):
    """
    Works out whether to apply form-controls class to a field on a form.

    :param field: The field to analyse
    :return: bool
    """
    apply_form_controls_to = [
        'TextInput',
        'PasswordInput',
        'EmailInput',
        'SelectInput',
    ]
    return field.field.widget.__class__.__name__ in apply_form_controls_to


@register.filter
def is_hidden(field):
    """
    Returns true is field is hidden
    """
    hidden_fields = [
        'HiddenInput',
    ]
    return field.field.widget.__class__.__name__ in hidden_fields


@register.filter
def is_checkbox(field):
    """
    Returns true if the field is a checkbox.
    """
    checkbox_fields = [
        'CheckboxInput',
    ]
    return field.field.widget.__class__.__name__ in checkbox_fields
