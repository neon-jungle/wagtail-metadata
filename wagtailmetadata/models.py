from django.db import models
from django.utils.translation import ugettext_lazy
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

    def get_meta_image(self):
        """
        Get the image to use for this object.
        Can be None if there is no relevant image.
        """
        return None

    def get_meta_twitter_card_type(self):
        """
        Get the Twitter card type for this object.
        See https://dev.twitter.com/cards/types.
        Defaults to 'summary_large_image' if the object has an image,
        otherwise 'summary'.
        """
        if self.get_meta_image() is not None:
            return 'summary_large_image'
        else:
            return 'summary'


class MetadataPageMixin(MetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=ugettext_lazy('Search image')
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
