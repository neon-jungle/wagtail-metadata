from django import template
from wagtailmetadata import tags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    request = context['request']
    if not model:
        model = context['self']

    return tags.meta_tags(request, model)
