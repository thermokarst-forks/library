import unittest

from django import test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from library.plugins.models import Plugin

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
    # @classmethod
    # def setUpTestData(cls):
    #     cls.author = User.objects.create_user('author', **{**_BASE_USER, 'forum_external_id': '1'})
    #     cls.author.groups.add(Group.objects.get(name='forum_trust_level_1'))
    #     cls.anon = User.objects.create_user('anon', **{**_BASE_USER, 'forum_external_id': '2'})

    #     cls.published_plugin_1 = Plugin.unsafe.create(
    #         **{**_BASE_PLUGIN, 'title': 'published_plugin_1'})
    #     cls.published_plugin_2 = Plugin.unsafe.create(
    #         **{**_BASE_PLUGIN, 'title': 'published_plugin_2'})
    #     cls.unpublished_plugin = Plugin.unsafe.create(
    #         **{**_BASE_PLUGIN, 'title': 'unpublished_plugin', 'published': False})

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
        plugin = Plugin.unsafe.create( **{**_BASE_PLUGIN, 'title': 'published_plugin'})

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


class LoggedInUserAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_plugin_list_no_unpublished(self):
        pass

    def test_plugin_list_some_unpublished(self):
        pass

    def test_plugin_detail_unpublished(self):
        pass

    def test_plugin_detail_published(self):
        pass

    def test_plugin_new(self):
        pass

    def test_plugin_edit_unpublished(self):
        pass

    def test_plugin_edit_published(self):
        pass


class AuthorAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_plugin_list_one_unpublished(self):
        pass

    def test_plugin_list_one_published(self):
        pass

    def test_plugin_list_published_and_unpublished(self):
        pass

    def test_plugin_detail_unpublished_not_coauthor(self):
        pass

    def test_plugin_detail_unpublished_is_coauthor(self):
        pass

    def test_plugin_detail_published_not_coauthor(self):
        pass

    def test_plugin_detail_published_is_coauthor(self):
        pass

    def test_plugin_new(self):
        pass

    def test_plugin_edit_unpublished_not_coauthor(self):
        pass

    def test_plugin_edit_unpublished_is_coauthor(self):
        pass

    def test_plugin_edit_published_not_coauthor(self):
        pass

    def test_plugin_edit_published_is_coauthor(self):
        pass


class AdminAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_plugin_list_no_unpublished(self):
        pass

    def test_plugin_list_some_unpublished(self):
        pass

    def test_plugin_detail_unpublished(self):
        pass

    def test_plugin_detail_published(self):
        pass

    def test_plugin_new(self):
        pass

    def test_plugin_edit_unpublished(self):
        pass

    def test_plugin_edit_published(self):
        pass
