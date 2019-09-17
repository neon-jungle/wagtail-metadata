from django import template

from wagtailmetadata import tags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    request = context.get('request', None)
    if not model:
        model = context.get('self', None)

    return tags.meta_tags(request, model)
