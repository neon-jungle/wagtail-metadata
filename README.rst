===============
wagtail-metadata
===============

A tool to assist with metadata for social media and search engines.

Installing
==========

Install using pip::

    pip install wagtail-metadata

It works with Wagtail 1.0 and upwards.


Using
=====

This module will add a link in your settings panel labeled 'Metadata'. From there you will be able to set site wide preferences that all pages will default to. To have per page meta descriptions and images, you'll need to inherit from ``wagtailmetadata.models.MetadataPageMixin``. This will add one extra field to your promote tab. The field 'Search description' will be your meta description, and 'Search image' will be your meta image.

Ensure you put ``MetadataPageMixin`` before ``Page``, for example.

.. code-block:: python

    from wagtail.wagtailcore.models import Page
    from wagtailmetadata.models import MetadataPageMixin

    class ContentPage(MetadataPageMixin, Page):
        pass

Display
=======

To use this in your template, you will firstly need to include the template tag library, and then insert the template tag ``{% meta_tags %}`` into your ``<head>``, see below for an example.

.. code-block:: html

    {% load wagtailmetadata_tags %}
    {% meta_tags %}

The tags will not display if you haven't defined a ``SiteMetadataPreferences`` object (by filling out the fields in wagtail), and a warning will be issued in the terminal until they have been defined.

It is important to note that the template tag expects to be used where self is in the context as an instance of a wagtail page, so using the template tag where this is not the case will cause some of the meta tags to blank or not work.
