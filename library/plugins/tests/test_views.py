import unittest
from django import test


class AnonymousUserAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_plugin_list_no_unpublished(self):
        response = self.client.get('/plugins/')

        self.assertEqual(response.status_code, 200)
        # TODO: Add in plugins into test DB
        self.assertEqual(len(response.context['plugins']), 2)

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
