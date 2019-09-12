from django import template

from wagtailmetadata import tags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    if 'request' in context:
        request = context['request']
        if not model and 'self' in context:
            model = context['self']
        if model:
            return tags.meta_tags(request, model)
    return ''
