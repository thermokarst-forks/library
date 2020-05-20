from django import test


class ViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_debug_celery_view(self):
        response = self.client.get('/_debug?hello=world')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context, None)
        self.assertTrue(b"{'hello': 'world'}" in response.content)
