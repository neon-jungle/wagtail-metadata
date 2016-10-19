from django.conf import settings
from django.template.loader import render_to_string


def get_meta_image_url(request, image):
    """
    Resize an image for metadata tags, and return an absolute URL to it.
    """
    rendition = image.get_rendition(filter='original')
    return request.build_absolute_uri(rendition.url)


def meta_tags(request, model):
    context = {
        'site_name': request.site.site_name,
        'object': model,
    }

    meta_image = model.get_meta_image()
    if meta_image:
        meta_image = get_meta_image_url(request, meta_image)
    context['meta_image'] = meta_image

    return render_to_string('wagtailmetadata/parts/tags.html', context)
