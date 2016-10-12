from django import template
from wagtailmetadata import tags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model_name):
    request = context['request']
    if model_name:
        page = context[model_name]
    else:
        page = context['self']

    return tags.meta_tags(request, page)
