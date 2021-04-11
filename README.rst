================
wagtail-metadata
================

.. image:: https://gitlab.com/neonjungle/wagtail-metadata/badges/master/pipeline.svg
    :target: https://gitlab.com/neonjungle/wagtail-metadata/pipelines?ref=master

This plugin adds custom properties to your page models and then lets you output meta-attribute tags  using the included template tag.
These tags help with search engine optimisations and for creating nice shareable links for social media, mainly Facebook and Twitter.


Compatibility
=============

Wagtail-metadata works with Wagtail v2.0 and upwards.

Installing
==========

First, install using pip::

    pip install wagtail-metadata

Then add ``wagtailmetadata`` to your project's ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        'home',
        'search',
        # etc...

        'wagtail.contrib.settings',
        'wagtail.contrib.modeladmin',
        # etc...

        # Add the following:
        'wagtailmetadata',

    ]

Using
=====

Pages should inherit from ``wagtailmetadata.models.MetadataPageMixin``.
This provides a ``search_image`` field in the Wagtail interface for that page type.
The description for the page will be pulled from the ``search_description`` page.
Metadata for the page will then be built from the page details.


.. code-block:: python

    from wagtail.core.models import Page
    from wagtailmetadata.models import MetadataPageMixin

    class ContentPage(MetadataPageMixin, Page):
        pass

.. note::

    Ensure you put ``MetadataPageMixin`` before ``Page``.

If you want to use this with a non-page model,
or want to use a different implementation for the fields,
you can inherit from ``wagtailmetadata.models.MetadataMixin``.
You will need to implement the following methods:

.. code-block:: python

    from wagtailmetadata.models import MetadataMixin

    class CustomObject(MetadataMixin, object):
        def get_meta_title(self):
            """The title of this object"""
            return "My custom object"

        def get_meta_url(self):
            """The URL of this object, including protocol and domain"""
            return "http://example.com/my-custom-object/"

        def get_meta_description(self):
            """
            A short text description of this object.
            This should be plain text, not HTML.
            """
            return "This thing is really cool, you should totally check it out"

        def get_meta_image_url(self, request):
            """
            Return a url for an image to use, see the MetadataPageMixin if using a Wagtail image
            """
            return 'https://neonjungle.studio/share.png'

        def get_meta_twitter_card_type(self):
            """
            What kind of Twitter card to show this as.
            Defaults to ``summary_large_photo`` if there is a meta image,
            or ``summary`` if there is no image. Optional.
            """
            return "summary_large_photo"

If your custom object uses Wagtail images, you may wish to use the intermediary mixin ``wagtailmetadata.models.WagtailImageMetadataMixin``
so you can use the relationship for the image related metadata:

.. code-block:: python

    from django.db import models
    from wagtailmetadata.models import WagtailImageMetadataMixin
    
    class CustomObject(WagtailImageMetadataMixin, object):
        share_image = models.ForeignKey('wagtailimages.Image', ondelete=models.SET_NULL, null=True, related_name='+')

        def get_meta_image(self):
            return self.share_image


Display
=======

Django
------

To use this in a template, first load the template tag library,
and then insert the metadata by placing ``{% meta_tags %}`` into the ``<head>``:

.. code-block:: html+django

    {% load wagtailmetadata_tags %}
    {% meta_tags %}

By default, this will look for a ``self`` object in the context to pull the metadata from.
You can specify a different object to use if you need to:

.. code-block:: html+django

    {% load wagtailmetadata_tags %}
    {% meta_tags my_custom_object %}

Jinja2
------

Add ``wagtailmetadata.jinja2tags.WagtailMetadataExtension`` to the template extensions
in your ``settings.py``:

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'OPTIONS': {
                'extensions': [
                    'wagtailmetadata.jinja2tags.WagtailMetadataExtension'
                ],
            },
        }
    ]

Insert the metadata by placing ``{{ meta_tags() }}`` into the ``<head>``:

.. code-block:: html

    {{ meta_tags() }}

By default, this will look for a ``page`` object in the context to pull the metadata from.
You can specify a different object to use if you need to:

.. code-block:: html

    {{ meta_tags(my_custom_object) }}


Troubleshooting
===============

`'meta_tags' missing request from context`

The template that is trying to render the `meta_tags` tag does not have a `request` object in the context. 

`'meta_tags' tag is missing a model or object`

There was no model passed to the template tag, or `self` is not found in the current context.


Adding extra tags
=================

If you need to add extra meta tags, to add the twitter:site tag for example,
you can extend the Wagtail Metadata template.
First, create any models that you might need to hold the extra data:

.. code-block:: python

    from wagtail.contrib.settings.models import BaseSetting, register_setting

    @register_setting
    class TwitterName(BaseSetting):
        handle = models.CharField(max_length=20)

You could also add extra fields to a page model and output them as meta tags:

.. code-block:: python

    class MyPage(MetadataPageMixin, Page):
        body = RichTextField()
        author_twitter_handle = models.CharField(max_length=20)

Then, override the ``wagtailmetadata/parts/tags.html`` template
and add your tags to the relevant blocks:

.. code-block:: html

    {% extends "wagtailmetadata/parts/tags.html" %}

    {% block twitter %}
        {{ block.super }}
        <meta name="twitter:site" content="@{{ settings.myapp.TwitterName.twitter_handle }}" />
        <meta name="twitter:creator" content="@{{ model.author_twitter_handle }}" />
    {% endblock %}

The ``wagtailmetadata/parts/tags.html`` template defines the following blocks
you can override or extend:

``{% block tags %}``
    This block surrounds the whole template.
    You can override this block to append extra tags before or after the standard tags.

``{% block twitter %}``
    This block surrounds the Twitter card tags.

``{% block opengraph %}``
    This block surrounds the Open Graph tags

``{% block meta %}``
    This block surrounds the standard meta tags defined in HTML.
