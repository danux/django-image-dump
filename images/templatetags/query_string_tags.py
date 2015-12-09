# -*- coding: utf-8 -*-
"""
Template tag that allows the query string to be manipulated in the templates.
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


class QueryStringManipulator(object):
    """
    Allows the query string to be manipulated, used for building up filter lists.
    """

    @staticmethod
    def get_query_string(params, new_params=None, remove=None):
        """
        Add and remove query parameters. From `django.contrib.admin`.

        :param params: The existing query string parameters
        :type params: {}

        :param new_params: Parameters to add to the query sting.
        :type new_params: {}

        :param remove: Parameters to remove
        :type remove: ()
        """
        if new_params is None:
            new_params = {}
        if remove is None:
            remove = []

        for prefix in remove:
            # Re-create params, excluding all keys that start with what we are removing
            params = {key: value for (key, value) in params.items() if not key.startswith(prefix)}

        for key, new_value in new_params.items():
            if new_value is None:
                try:
                    del params[key]
                except KeyError:
                    # Key was already absent
                    pass
            else:
                params[key] = new_value

        return mark_safe('?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in sorted(params.items())]).replace(' ', '%20'))

    @staticmethod
    def string_to_dict(to_split, variable_value=None):
        """
        Converts a string in to a dict.

        :type to_split: string or unicode
        :param variable_value: Allows a variable from the context to be passed in, i.e. the page number.
        """
        kwargs = {}
        for arg in QueryStringManipulator.string_to_list(to_split):
            kw, val = arg.split('=', 1)
            if variable_value is not None and val == "var":
                kwargs[kw] = variable_value
            else:
                kwargs[kw] = val
        return kwargs

    @staticmethod
    def string_to_list(to_split):
        """
        Converts a string to a list.

        :type to_split: str or unicode
        """
        # Split on commas and remove extraneous whitespace
        sub_strings = [substring.strip() for substring in to_split.split(",")]
        # Return all non-empty items
        return [substring for substring in sub_strings if substring]


@register.inclusion_tag('includes/query_string.html', takes_context=True)
def query_string(context, add=None, remove=None, variable_value=None):
    """
    Allows the addition and removal of query string parameters.
    Written as an inclusion tag to simplify getting the context.

    :type context: {}
    :type add: str or unicode
    :type remove: str or unicode
    :type variable_value: str or unicode

    query_string.html is just {{ response }}

    Usage:
    http://www.url.com/{% query_string "param_to_add=value, param_to_add=value" "param_to_remove, params_to_remove" %}
    http://www.url.com/{% query_string "" "filter" %}filter={{new_filter}}
    http://www.url.com/{% query_string "sort=value" "sort" %}

    "sort=value" as add value does not allow for dynamic values from the context. To add a value from the context
    as parameter value you must set the add value to var.

    http://www.url.com/{% query_string "page=var" "" paginator.current_page %}
    """
    add = QueryStringManipulator.string_to_dict(add, variable_value)
    remove = QueryStringManipulator.string_to_list(remove)
    params = dict(context['request'].GET.items())
    response = QueryStringManipulator.get_query_string(params, add, remove)
    return {'response': response}
