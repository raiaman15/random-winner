from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views


class PoolCreateTests(SimpleTestCase):

    def setUp(self):
        url = reverse('pool_create')
        self.response = self.client.get(url)

    def test_poolcreate_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_poolcreate_template(self):
        self.assertTemplateUsed('pages/product.html')

    def test_poolcreate_contains_correct_html(self):
        self.assertContains(self.response, 'All Rights Reserved')

    def test_poolcreate_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_poolcreate_url_resolves_poolcreateview(self):
        view = resolve('pool/create/')
        self.assertEqual(view.func.__name__, views.PoolCreateView.as_view().__name__)
