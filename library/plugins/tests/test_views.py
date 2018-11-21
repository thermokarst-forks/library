from django import test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from library.plugins.models import Plugin, PluginAuthorship

User = get_user_model()

_BASE_USER = {
    'email': '',
    'password': '',
    'full_name': '',
    'forum_external_id': '',
    'forum_avatar_url': 'https://qiime2.org',
    'forum_is_admin': False,
    'forum_is_moderator': False,
}


_BASE_PLUGIN = {
    'title': 'plugin',
    'short_summary': 'lorem ipsum summary',
    'description': 'lorem ipsum description',
    'install_guide': 'lorem ipsum install',
    'published': True,
    'source_url': 'https://qiime2.org',
    'version': '0.1.4',
}


class AnonymousUserAuthorizationTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_plugin_list_no_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_2'})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_list_some_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_2'})
        Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_detail_unpublished(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/' % plugin.slug)

        self.assertEqual(response.status_code, 404)

    def test_plugin_detail_published(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_new(self):
        response = self.client.get('/plugins/new/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/plugins/new/')

    def test_plugin_edit_unpublished(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/edit/' % plugin.slug)

        self.assertEqual(response.status_code, 404)

    def test_plugin_edit_published(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/edit/' % plugin.slug)

        self.assertEqual(response.status_code, 404)


class LoggedInUserAuthorizationTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'user',
            **{**_BASE_USER, 'forum_external_id': '1', 'password': 'peanut'})

    def setUp(self):
        self.client = test.Client()
        self.client.login(username='user', password='peanut')

    def test_plugin_list_no_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_2'})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_list_some_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_2'})
        Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_detail_unpublished(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/' % plugin.slug)

        self.assertEqual(response.status_code, 404)

    def test_plugin_detail_published(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_new(self):
        response = self.client.get('/plugins/new/')

        self.assertEqual(response.status_code, 403)

    def test_plugin_edit_unpublished(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/edit/' % plugin.slug)

        self.assertEqual(response.status_code, 404)

    def test_plugin_edit_published(self):
        plugin = Plugin.unsafe.create(
                **{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/edit/' % plugin.slug)

        self.assertEqual(response.status_code, 404)


class AuthorAuthorizationTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'author',
            **{**_BASE_USER, 'forum_external_id': '1', 'password': 'peanut'})
        cls.user.groups.add(Group.objects.get(name='forum_trust_level_1'))

    def setUp(self):
        self.client = test.Client()
        self.client.login(username='author', password='peanut')

    def test_plugin_list_one_unpublished(self):
        unpublished = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})
        PluginAuthorship.objects.create(plugin=unpublished, author=self.user, list_position=0)

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 1)

    def test_plugin_list_one_published(self):
        p = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})
        PluginAuthorship.objects.create(plugin=p, author=self.user, list_position=0)

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 1)

    def test_plugin_list_published_and_unpublished(self):
        p1 = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})
        PluginAuthorship.objects.create(plugin=p1, author=self.user, list_position=0)
        p2 = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})
        PluginAuthorship.objects.create(plugin=p2, author=self.user, list_position=0)

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_detail_unpublished_not_coauthor(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 404)

    def test_plugin_detail_unpublished_is_coauthor(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})
        PluginAuthorship.objects.create(plugin=plugin, author=self.user, list_position=0)

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_detail_published_not_coauthor(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_detail_published_is_coauthor(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})
        PluginAuthorship.objects.create(plugin=plugin, author=self.user, list_position=0)

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_new(self):
        response = self.client.get('/plugins/new/')

        self.assertEqual(response.status_code, 200)

    def test_plugin_edit_unpublished_not_coauthor(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 404)

    def test_plugin_edit_unpublished_is_coauthor(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})
        PluginAuthorship.objects.create(plugin=plugin, author=self.user, list_position=0)

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_edit_published_not_coauthor(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 404)

    def test_plugin_edit_published_is_coauthor(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'unpublished_plugin'})
        PluginAuthorship.objects.create(plugin=plugin, author=self.user, list_position=0)

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)


class AdminAuthorizationTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'admin',
            **{**_BASE_USER, 'forum_external_id': '1', 'password': 'peanut',
               'is_superuser': True, 'forum_is_admin': True})

    def setUp(self):
        self.client = test.Client()
        self.client.login(username='admin', password='peanut')

    def test_plugin_list_no_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin_2'})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_list_some_unpublished(self):
        Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'published_plugin'})
        Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['plugins']), 2)

    def test_plugin_detail_unpublished(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_detail_published(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'unpublished_plugin'})

        response = self.client.get('/plugins/%s/%d/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_new(self):
        response = self.client.get('/plugins/new/')

        self.assertEqual(response.status_code, 200)

    def test_plugin_edit_unpublished(self):
        plugin = Plugin.unsafe.create(
            **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)

    def test_plugin_edit_published(self):
        plugin = Plugin.unsafe.create(**{**_BASE_PLUGIN, 'title': 'unpublished_plugin'})

        response = self.client.get('/plugins/%s/%d/edit/' % (plugin.slug, plugin.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plugin'], plugin)
