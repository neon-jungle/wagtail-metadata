import warnings

from django.conf import settings
from django.template.loader import render_to_string
from wagtail.wagtailcore.models import Site
from wagtailmetadata.models import SiteMetadataPreferences


def meta_tags(request, page):
    site = Site.find_for_request(request)
    try:
        global_settings = SiteMetadataPreferences.objects.get(site=site)
    except SiteMetadataPreferences.DoesNotExist:
        warnings.warn('Your global metadata settings are not defined for {0}'.format(site))
        return ''

    page.meta_image = page.search_image or global_settings.site_image
    page.meta_description = page.search_description or global_settings.site_description

    if page.meta_image:
        page.meta_image = page.meta_image.get_rendition(filter='original')
        page.meta_image.full_url = request.build_absolute_uri(page.meta_image.url)

    page.absolute_url = request.build_absolute_uri(page.url)
    return render_to_string('wagtailmetadata/parts/tags.html', {
        'page': page,
        'site_name': settings.WAGTAIL_SITE_NAME,
        'global_settings': global_settings,
    })
