from django.test import TestCase
from wagtail.core.models import Site
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file

from tests.app.models import TestPage


class TestMetadataPageMixin(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.site.site_name = 'Example site'
        self.site.save()

        self.image = Image.objects.create(
            title='Test Image',
            file=get_test_image_file(),
        )
        self.page = self.site.root_page.add_child(instance=TestPage(
            title='Test Page',
            search_image=self.image,
            search_description='Some test content description',
        ))

    def test_title(self):
        self.assertEqual(
            self.page.get_meta_title(),
            'Test Page')

    def test_url(self):
        self.assertEqual(
            self.page.get_meta_url(),
            'http://localhost/test-page/')

    def test_description(self):
        self.assertEqual(
            self.page.get_meta_description(),
            'Some test content description')

    def test_image(self):
        self.assertEqual(
            self.page.get_meta_image(),
            self.image)
