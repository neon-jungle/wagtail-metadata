from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from wagtail.core.models import Site


def get_meta_image_url(request, image):
    """
    Resize an image for metadata tags, and return an absolute URL to it.
    """
    filter = getattr(settings, "WAGTAILMETADATA_IMAGE_FILTER", "original")
    rendition = image.get_rendition(filter=filter)
    return request.build_absolute_uri(rendition.url)


def meta_tags(request, model):
    if not request:
        raise TemplateSyntaxError(
            "'meta_tags' missing request from context")
    if not model:
        raise TemplateSyntaxError(
            "'meta_tags' tag is missing a model or object")
    context = {
        'site_name': Site.find_for_request(request).site_name,
        'object': model,
    }

    meta_image = model.get_meta_image()
    if meta_image:
        meta_image = get_meta_image_url(request, meta_image)
    context['meta_image'] = meta_image

    return render_to_string('wagtailmetadata/parts/tags.html',
                            context, request=request)
