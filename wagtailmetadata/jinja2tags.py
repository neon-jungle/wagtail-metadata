import jinja2
import markupsafe
from jinja2.ext import Extension

from wagtailmetadata import tags


@jinja2.pass_context
def meta_tags(context, model=None):
    request = context.get('request', None)
    if not model:
        model = context.get('page', None)

    return markupsafe.Markup(tags.meta_tags(request, model))


class WagtailMetadataExtension(Extension):
    def __init__(self, environment):
        super(WagtailMetadataExtension, self).__init__(environment)

        self.environment.globals.update({
            'meta_tags': meta_tags,
        })
