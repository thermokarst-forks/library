from django import test

from django.test.utils import override_settings


class ViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_debug_celery_view(self):
        response = self.client.get('/_debug?hello=squirrel')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context, None)
        self.assertTrue(b"{'hello': 'squirrel'}" in response.content)
