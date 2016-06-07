import warnings

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from wagtail.wagtailcore.models import Site
from wagtailmetadata.models import SiteMetadataPreferences

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context):
    instance = context['self']
    request = context['request']
    page = context['self']
    site = Site.find_for_request(request)
    try:
        global_settings = SiteMetadataPreferences.objects.get(site=site)
    except SiteMetadataPreferences.DoesNotExist:
        warnings.warn('Your global metadata settings are not defined for {0}'.format(site))
        return ''

    instance.meta_image = instance.search_image or global_settings.site_image
    instance.meta_description = instance.search_description or global_settings.site_description

    if instance.meta_image:
        instance.meta_image = instance.meta_image.get_rendition(filter='original')
        instance.meta_image.full_url = request.build_absolute_uri(instance.meta_image.url)

    page.absolute_url = request.build_absolute_uri(page.url)
    return render_to_string('wagtailmetadata/parts/tags.html', {
        'instance': instance,
        'page': page,
        'site_name': settings.WAGTAIL_SITE_NAME,
        'global_settings': global_settings,
    })
