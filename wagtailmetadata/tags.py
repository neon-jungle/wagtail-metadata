from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from wagtail.core.models import Site


def meta_tags(request, model):
    if not request:
        raise TemplateSyntaxError(
            "'meta_tags' missing request from context")
    if not model:
        raise TemplateSyntaxError(
            "'meta_tags' tag is missing a model or object")
    context = {
        'site_name': Site.find_for_request(request).site_name,
        'twitter_card_type': model.get_twitter_card_type(request),
        'object': model,
    }

    meta_image = model.get_meta_image_url(request)
    if meta_image:
        width, height = model.get_meta_image_dimensions()
        context['meta_image_width'] = width
        context['meta_image_height'] = height
    context['meta_image'] = meta_image

    return render_to_string('wagtailmetadata/parts/tags.html',
                            context, request=request)
