from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class SiteMetadataPreferences(models.Model):
    site = models.OneToOneField(Site, unique=True, db_index=True, editable=False)
    site_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)
    site_description = models.TextField()

    panels = [
        ImageChooserPanel('site_image'),
        FieldPanel('site_description')
    ]


class MetadataPageMixin(models.Model):
    page_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)
    page_description = models.TextField(blank=True)

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            ImageChooserPanel('page_image'),
            FieldPanel('page_description')], heading='Social Media Metadata')
    ]

    class Meta:
        abstract = True
