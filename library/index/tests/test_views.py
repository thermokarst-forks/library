from django import test

from django.test.utils import override_settings


class ViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    # @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    #                    CELERY_ALWAYS_EAGER=True)
    # def test_debug_celery_view(self):
    #     response = self.client.get('/_debug?hello=world')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context, None)
    #     self.assertTrue(b"{'hello': 'world'}" in response.content)
