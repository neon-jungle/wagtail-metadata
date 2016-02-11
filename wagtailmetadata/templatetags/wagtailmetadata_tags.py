from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import format_html
from wagtail.wagtailcore.models import Site
from wagtailmetadata.models import SiteMetadataPreferences

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context):
    instance = context['self']
    request = context['request']
    site = Site.find_for_request(request)
    if not instance.page_image and not instance.page_description:
        try:
            instance = SiteMetadataPreferences.objects.get(site=site)
        except SiteMetadataPreferences.DoesNotExist:
            return format_html('<!-- Please define your global metadata settings -->')
    return render_to_string('wagtailmetadata/parts/tags.html', {
        'instance': instance,
        'page': context['self'],
        'site_name': settings.WAGTAIL_SITE_NAME
    })


@register.simple_tag()
def tot(first, second):
    """
    This or that, here shortened to 'tot'
    will display a variable if it exists,
    and if it doesn't, will display the second
    variable passed through, and finally, none.
    """
    if first:
        return first
    elif second:
        return second
    else:
        return None
