from django import test
from django.test.utils import override_settings

from library.index.tasks import debug


class DebugTestCase(test.TestCase):
    def test_debug_task(self):
        result = debug.delay({'hello': 'world'})
        obs = result.get(timeout=1)
        self.assertTrue(result.successful())
        self.assertEqual(obs, {'hello': 'world'})
