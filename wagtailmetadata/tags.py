import warnings

from django.conf import settings
from django.template.loader import render_to_string
from wagtail.wagtailcore.models import Site
from wagtailmetadata.models import SiteMetadataPreferences


def get_meta_image_url(request, image):
    """
    Resize an image for metadata tags, and return an absolute URL to it.
    """
    rendition = image.get_rendition(filter='original')
    return request.build_absolute_uri(rendition.url)


def meta_tags(request, model):
    site = Site.find_for_request(request)

    context = {
        'site_name': settings.WAGTAIL_SITE_NAME,
        'meta_title': model.get_meta_title(),
        'meta_url': model.get_meta_url(),
    }

    try:
        global_settings = SiteMetadataPreferences.objects.get(site=site)
        context['global_settings'] = global_settings
    except SiteMetadataPreferences.DoesNotExist:
        warnings.warn('Your global metadata settings are not defined for {0}'
                      .format(site))
        global_settings = None
    context['global_settings'] = global_settings

    # Search image/description have fallback if the global settings exist
    meta_image = model.get_meta_image()
    if meta_image:
        meta_image = get_meta_image_url(request, meta_image)
    elif global_settings and global_settings.site_image:
        meta_image = get_meta_image_url(request, global_settings.site_image)
    context['meta_image'] = meta_image

    meta_description = model.get_meta_description()
    if not meta_description and \
            global_settings and global_settings.site_description:
        context['meta_description'] = global_settings.site_description
    else:
        context['meta_description'] = meta_description

    return render_to_string('wagtailmetadata/parts/tags.html', context)
