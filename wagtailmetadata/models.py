from django.db import models
from django.utils.translation import ugettext_lazy
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.models import Site
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from .utils import get_image_model_string

TWITTER_CARD_TYPES = [
    ('summary', 'Summary card'),
    ('summary_large_image', 'Summary card with large image'),
]


class SiteMetadataPreferences(models.Model):
    site = models.OneToOneField(Site, unique=True, db_index=True, editable=False)

    # Twitter settings
    card_type = models.CharField(max_length=128, choices=TWITTER_CARD_TYPES)

    twitter_panels = [
        MultiFieldPanel([
            FieldPanel('card_type')
        ], heading='Twitter')
    ]


class MetadataMixin(object):
    def get_meta_url(self):
        raise NotImplementedError()

    def get_meta_title(self):
        raise NotImplementedError()

    def get_meta_description(self):
        raise NotImplementedError()

    def get_meta_image(self):
        raise NotImplementedError()


class MetadataPageMixin(MetadataMixin, models.Model):
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], ugettext_lazy('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_image(self):
        return self.search_image

    class Meta:
        abstract = True
