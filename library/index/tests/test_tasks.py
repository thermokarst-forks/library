from django import test
from django.test.utils import override_settings

from library.index.tasks import debug


class DebugTestCase(test.TestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True)
    def test_debug_task(self):
        result = debug.delay({'hello': 'world'})
        print('hello', result)
        self.assertTrue(result.successful())
