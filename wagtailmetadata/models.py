from django.db import models
from django.utils.translation import ugettext_lazy
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

TWITTER_CARD_TYPES = [
    ('summary', 'Summary card'),
    ('summary_large_image', 'Summary card with large image'),
]


class SiteMetadataPreferences(models.Model):
    site = models.OneToOneField(Site, unique=True, db_index=True, editable=False)
    site_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="""
        This is the default image that will be shown when your page is
         shared on social media or is found on search engines """)
    site_description = models.TextField(help_text="""
    This is the default description displayed when your page is shared on
     social media or is found on search engines""")

    # Twitter settings
    card_type = models.CharField(max_length=128, choices=TWITTER_CARD_TYPES)

    general_panels = [
        MultiFieldPanel([
            ImageChooserPanel('site_image'),
            FieldPanel('site_description')
        ], heading='General')
    ]

    twitter_panels = [
        MultiFieldPanel([
            FieldPanel('card_type')
        ], heading='Twitter')
    ]


class MetadataPageMixin(models.Model):
    search_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], ugettext_lazy('Common page configuration')),
    ]

    class Meta:
        abstract = True
