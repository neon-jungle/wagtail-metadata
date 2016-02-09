from django import template
from django.template.loader import render_to_string
from wagtail.wagtailcore.models import Site
from wagtailmetadata.models import SiteMetadataPreferences

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context):
    instance = context['self']
    request = context['request']
    if instance.page_image or instance.site_description:
        pass
    else:
        site = Site.find_for_request(request)
        instance = SiteMetadataPreferences(site=site)
    return render_to_string('wagtailmetadata/parts/tags.html', {
        'instance': instance
    })

# TODO
