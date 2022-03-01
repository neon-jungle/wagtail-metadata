from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from .utils import get_image_model_string


class MetadataMixin(object):
    """
    An object that can be shared on social media.
    """

    def get_meta_url(self):
        """The full URL to this object, including protocol and domain."""
        raise NotImplementedError()

    def get_meta_title(self):
        raise NotImplementedError()

    def get_object_title(self):
        return self.get_meta_title()

    def get_meta_description(self):
        raise NotImplementedError()

    def get_meta_image_url(self, request):
        """
        Get the image url to use for this object.
        Can be None if there is no relevant image.
        """
        return None

    def get_meta_image_dimensions(self):
        """
        Return width, height (in pixels)
        """
        return None, None

    def get_twitter_card_type(self, request):
        """
        Get the Twitter card type for this object.
        See https://dev.twitter.com/cards/types.
        Defaults to 'summary' if the object has an image,
        otherwise 'summary'.
        """
        if self.get_meta_image_url(request) is not None:
            return 'summary_large_image'
        else:
            return 'summary'


class WagtailImageMetadataMixin(MetadataMixin):
    """
    Subclass of MetadataMixin that uses a Wagtail Image for the image-based metadata
    """
    def get_meta_image(self):
        raise NotImplementedError()

    def get_meta_image_rendition(self):
        meta_image = self.get_meta_image()
        if meta_image:
            filter = getattr(settings, "WAGTAILMETADATA_IMAGE_FILTER", "original")
            rendition = meta_image.get_rendition(filter=filter)
            return rendition
        return None

    def get_meta_image_url(self, request):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return request.build_absolute_uri(meta_image.url)
        return None

    def get_meta_image_dimensions(self):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return meta_image.width, meta_image.height
        return None, None


class MetadataPageMixin(WagtailImageMetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=gettext_lazy('Search image')
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], gettext_lazy('Common page configuration')),
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
