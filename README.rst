===============
wagtail-metadata
===============

A tool to assist with metadata for social media.

Installing
==========

Install using pip::

    pip install wagtail-metadata

It works with Wagtail 1.0 and upwards.


Using
=====

This module will add a link in your settings panel labeled 'Meta Data'. From there you will be able to set site wide preferences
that all pages will default to. To have per page meta descriptions and images, you'll need to inherit from ``wagtailmetadata.models.MetadataPageMixinPage``.
This will add one extra field to your promote tab. The field `Search description` will be your meta description, and 'Search image' will be your
meta image.

Display
=======

To use this in your template, you will firstly need to include the template tag library, and then use it, see below for an example.

.. code-block:: html

    {% load wagtailmetadata_tags %}
    {% meta_tags %}


It is important to note that the template tag expects this to be used where self is in the context as an instance of a wagtail packages,
so using the template tag where this is not the case will cause some of the meta tags to blank or not work.
