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
        'object': model,
    }

    try:
        global_settings = SiteMetadataPreferences.objects.get(site=site)
        context['global_settings'] = global_settings
    except SiteMetadataPreferences.DoesNotExist:
        warnings.warn('Your global metadata settings are not defined for {0}'
                      .format(site))
        global_settings = None
    context['global_settings'] = global_settings

    meta_image = model.get_meta_image()
    if meta_image:
        meta_image = get_meta_image_url(request, meta_image)
    context['meta_image'] = meta_image

    return render_to_string('wagtailmetadata/parts/tags.html', context)
