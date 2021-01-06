from django.db import models
from wagtail.core.models import Page

from wagtailmetadata.models import MetadataMixin, MetadataPageMixin


class TestPageBase(type(Page)):
    """See https://code.djangoproject.com/ticket/27337"""
    pass


class TestPage(MetadataPageMixin, Page, metaclass=TestPageBase):
    pass


class TestModel(MetadataMixin, models.Model):
    def get_meta_url(self):
        return 'http://takeflight.com.au'

    def get_meta_title(self):
        return 'Sharing on the big blue'

    def get_meta_description(self):
        return 'Wagtail 101 - A journey through a CMS (Corrective Monkey Surgery)'

    def get_meta_image_url(self, request):
        return None
