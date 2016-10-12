from django.conf import settings
from django.forms.utils import flatatt
from django.template import engines
from django.test import RequestFactory, TestCase
from django.utils.html import format_html
from wagtail.wagtailcore.models import Site
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.tests.utils import get_test_image_file
from wagtailmetadata.models import SiteMetadataPreferences
from wagtailmetadata.tags import get_meta_image_url

from tests.app.models import TestModel, TestPage


class TemplateCase(object):

    def setUp(self):
        self.site = Site.objects.first()

        self.factory = RequestFactory()
        self.request = self.factory.get('/test/')
        self.request.site = self.site

        self.image = Image.objects.create(title='Test Image', file=get_test_image_file())
        self.settings = SiteMetadataPreferences.objects.create(
            site=self.site,
            site_image=self.image,
            card_type='summary',
            site_description='Site description'
        )
        self.page = self.site.root_page.add_child(instance=TestPage(title='Test Page'))
        self.test_model = TestModel.objects.create()

    def render(self, string, context=None, request_context=True):
        if context is None:
            context = {}

        # Add a request to the template, to simulate a RequestContext
        if request_context:
            context['request'] = self.request

        template = self.engine.from_string(string)
        return template.render(context)

    def meta(self, attrs):
        return format_html('<meta{0}>'.format(flatatt(attrs)))

    def test_twitter_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'name': 'twitter:card', 'content': self.settings.card_type
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:title', 'content': self.page.title
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:description', 'content': self.settings.site_description,
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:image',
            'content': get_meta_image_url(self.request, self.settings.site_image),
        }), out)

    def test_og_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'property': 'og:url', 'content': self.page.full_url
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:title', 'content': self.page.title
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:description', 'content': self.settings.site_description,
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:site_name', 'content': settings.WAGTAIL_SITE_NAME
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image',
            'content': get_meta_image_url(self.request, self.settings.site_image),
        }), out)

    def test_misc_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'itemprop': 'url', 'content': self.page.full_url
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'name', 'content': self.page.title
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'description', 'content': self.settings.site_description,
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'image',
            'content': get_meta_image_url(self.request, self.settings.site_image),
        }), out)

    def test_generic_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'name': 'description', 'content': self.settings.site_description,
        }), out)

    def test_custom_model(self):
        out = self.render_with_model()
        self.assertInHTML(self.meta({
            'itemprop': 'url',
            'content': self.test_model.get_meta_url()
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'name',
            'content': self.test_model.get_meta_title()
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'description',
            'content': self.test_model.get_meta_description()
        }), out)

    def fill_out_page_meta_fields(self):
        self.page.search_description = 'Hello, world'
        self.page.search_image = Image.objects.create(
            title='Page image', file=get_test_image_file())

    def test_page_twitter_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'name': 'twitter:description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:image',
            'content': get_meta_image_url(self.request, self.page.search_image),
        }), out)

    def test_page_og_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'property': 'og:description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image',
            'content': get_meta_image_url(self.request, self.page.search_image),
        }), out)

    def test_page_misc_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'itemprop': 'description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'image',
            'content': get_meta_image_url(self.request, self.page.search_image),
        }), out)

    def test_page_generic_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'name': 'description', 'content': self.page.search_description,
        }), out)


class TestJinja2(TemplateCase, TestCase):
    engine = engines['jinja2']

    def render_meta(self):
        return self.render('{{ meta_tags() }}', context={'page': self.page})

    def render_with_model(self):
        return self.render('{{ meta_tags(custom) }}', context={'custom': self.test_model})


class TestDjangoTemplateEngine(TemplateCase, TestCase):
    engine = engines['django']

    def render_meta(self):
        return self.render('{% load wagtailmetadata_tags %}{% meta_tags %}', context={'self': self.page})

    def render_with_model(self):
        return self.render('{% load wagtailmetadata_tags %}{% meta_tags custom %}', context={'custom': self.test_model})
