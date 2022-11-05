from django.forms.utils import flatatt
from django.template import TemplateSyntaxError, engines
from django.test import RequestFactory, TestCase, override_settings
from django.utils.html import format_html
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Site

from tests.app.models import TestModel, TestPage


class TemplateCase(object):

    def setUp(self):
        self.site = Site.objects.first()
        self.site.site_name = 'Example site'
        self.site.save()

        self.factory = RequestFactory()
        self.request = self.factory.get('/test/')
        self.request.site = self.site

        self.image = Image.objects.create(
            title='Test Image',
            file=get_test_image_file(),
        )
        self.page = self.site.root_page.add_child(instance=TestPage(
            title='Test Page',
            search_image=self.image,
            search_description='Some test content description',
        ))
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
            'name': 'twitter:card', 'content': 'summary_large_image',
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:title',
            'content': self.page.get_meta_title(),
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'name': 'twitter:image',
            'content': self.page.get_meta_image_url(self.request),
        }), out)

    def test_twitter_no_image(self):
        self.page.search_image = None
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'name': 'twitter:card', 'content': 'summary',
        }), out)
        self.assertNotIn('twitter:image', out)

    def test_og_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'property': 'og:url', 'content': self.page.full_url
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:title',
            'content': self.page.get_meta_title(),
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:site_name', 'content': self.site.site_name
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image',
            'content': self.page.get_meta_image_url(self.request),
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image:width',
            'content': self.page.get_meta_image_dimensions()[0]
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image:height',
            'content': self.page.get_meta_image_dimensions()[1]
        }), out)

    def test_og_no_image(self):
        self.page.search_image = None
        out = self.render_meta()
        self.assertNotIn('og:image', out)

    def test_misc_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'itemprop': 'url', 'content': self.page.full_url
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'name',
            'content': self.page.get_meta_title(),
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'image',
            'content': self.page.get_meta_image_url(self.request),
        }), out)
        self.assertInHTML(
            f'<title>{self.page.get_object_title()}</title>',
            out
        )

    def test_generic_render(self):
        out = self.render_meta()
        self.assertInHTML(self.meta({
            'name': 'description', 'content': self.page.search_description,
        }), out)

    def test_custom_model(self):
        out = self.render_with_model()
        self.assertInHTML(self.meta({
            'itemprop': 'url',
            'content': self.test_model.get_meta_url()
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'name',
            'content': self.test_model.get_meta_title(),
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
            'content': self.page.get_meta_image_url(self.request),
        }), out)

    def test_page_og_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'property': 'og:description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'property': 'og:image',
            'content': self.page.get_meta_image_url(self.request),
        }), out)

    def test_page_misc_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML(self.meta({
            'itemprop': 'description', 'content': self.page.search_description,
        }), out)
        self.assertInHTML(self.meta({
            'itemprop': 'image',
            'content': self.page.get_meta_image_url(self.request),
        }), out)

    def test_page_generic_render(self):
        self.fill_out_page_meta_fields()

        out = self.render_meta()

        self.assertInHTML("<title>{}</title>".format(self.page.title), out)
        self.assertInHTML(self.meta({
            'name': 'description', 'content': self.page.search_description,
        }), out)

    def test_error_messages(self):
        self.assertRaises(TemplateSyntaxError, self.render_with_error)

    def test_get_meta_image_url_filter(self):
        self.fill_out_page_meta_fields()

        result = self.page.get_meta_image_url(self.request)

        self.assertTrue(result.endswith("original.png"))

    @override_settings(WAGTAILMETADATA_IMAGE_FILTER="fill-10x20")
    def test_get_meta_image_url_filter_with_override(self):
        self.fill_out_page_meta_fields()

        result = self.page.get_meta_image_url(self.request)

        self.assertTrue(result.endswith("fill-10x20.png"))
        self.assertEqual((10, 20), self.page.get_meta_image_dimensions())


class TestJinja2(TemplateCase, TestCase):
    engine = engines['jinja2']

    def render_meta(self):
        return self.render('{{ meta_tags() }}', context={'page': self.page})

    def render_with_model(self):
        return self.render('{{ meta_tags(custom) }}', context={'custom': self.test_model})

    def render_with_error(self):
        return self.render('{{ meta_tags(custom) }}', context={'custom': None})


class TestDjangoTemplateEngine(TemplateCase, TestCase):
    engine = engines['django']

    def render_meta(self):
        return self.render('{% load wagtailmetadata_tags %}{% meta_tags %}', context={'self': self.page})

    def render_with_model(self):
        return self.render('{% load wagtailmetadata_tags %}{% meta_tags custom %}', context={'custom': self.test_model})

    def render_with_error(self):
        return self.render('{% load wagtailmetadata_tags %}{% meta_tags custom %}', context={'custom': None})
