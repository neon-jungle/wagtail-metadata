from wagtail.wagtailcore.models import Page
from wagtailmetadata.models import MetadataPageMixin


class TestPage(MetadataPageMixin, Page):
    pass
