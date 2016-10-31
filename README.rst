===============
wagtail-metadata
===============

A tool to assist with metadata for social media and search engines.

Installing
==========

Install using pip::

    pip install wagtail-metadata

It works with Wagtail 1.6 and upwards.

Using
=====

Pages should inherit from ``wagtailmetadata.models.MetadataPageMixin``.
This provides a ``search_image`` field in the Wagtail interface for that page type.
The description for the page will be pulled from the ``search_description`` page.
Metadata for the page will then be built from the page details.


.. code-block:: python

    from wagtail.wagtailcore.models import Page
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

        def get_meta_image(self):
            """A relevant Wagtail Image to show. Optional."""
            return self.some_image

        def get_meta_twitter_card_type(self):
            """
            What kind of Twitter card to show this as.
            Defaults to ``summary_large_photo`` if there is a meta image,
            or ``summary`` if there is no image. Optional.
            """
            return "summary_large_photo"


Display
=======

Django
------

To use this in a template, first load the template tag library,
and then insert the metadata by placing ``{% meta_tags %}`` into the ``<head>``:

.. code-block:: html

    {% load wagtailmetadata_tags %}
    {% meta_tags %}

By default, this will look for a ``self`` object in the context to pull the metadata from.
You can specify a different object to use if you need to:

.. code-block:: html

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
