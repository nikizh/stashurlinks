from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
import json
import populate_db
import stashmarksApp.models as models
import stashmarksProj


class ModelTests(TestCase):
    def test_ensure_tag_constructor(self):
        tag = models.Tag(name="Test")
        tag.save()
        self.assertEqual(tag.name, "Test")

    def test_ensure_bookmark_constructor(self):
        testUser = User()
        testUser.save()
        bm = models.Bookmark(title="Test", public=False, likes=1, owner=testUser)
        bm.save()
        self.assertEqual(bm.title, "Test")
        self.assertEqual(bm.public, False)
        self.assertEqual(bm.likes, 1)
        self.assertEqual(bm.owner, testUser)

    def test_ensure_ratings_constructor(self):
        testUser = User()
        testUser.save()
        bm = models.Bookmark(title="Test", public=False, likes=1, owner=testUser)
        bm.save()
        rating = models.Ratings(owner=testUser, bookmark=bm, liked=True)
        rating.save()
        self.assertEqual(rating.owner, testUser)
        self.assertEqual(rating.bookmark, bm)
        self.assertEqual(rating.liked, True)


class MyStashAddViewTests(TestCase):
    def test_malformed_url_input(self):
        """
        Test that we can handle malformed input, because
        some web servers compact %2F%2F to single forward slash.
        """

        # Test with single %2F to simulate malformed input
        response = self.client.get('/mystash/add/title/TEST123/url/http%3A%2Fbbc.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'TEST123')
        self.assertEqual(response.context['url'], 'http://bbc.com')


class RestAPITests(TestCase):
    def setUp(self):
        populate_db.populate()
        if 'allauth.socialaccount' in stashmarksProj.settings.INSTALLED_APPS:
            # Otherwise ImproperlyConfigured exceptions may occur
            from allauth.socialaccount.models import SocialApp

            sa = SocialApp.objects.create(name='testfb',
                                          provider='facebook')
            sa.sites.add(Site.objects.get_current())

    def test_get_all_tags(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/alltags/?format=json')

        self.assertEqual(response.status_code, 200)

    def test_get_all_bookmarks(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/allbookmarks/?format=json')

        self.assertEqual(response.status_code, 200)

    def test_get_all_bookmarks_by_likes(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/allbookmarks/?format=json&order=likes')

        self.assertEqual(response.status_code, 200)

    def test_get_bookmarks_by_tags(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/allbookmarks/?format=json&tags=python')

        self.assertEqual(response.status_code, 200)

    def test_get_bookmarks_by_text(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/allbookmarks/?format=json&q=pyt')

        self.assertEqual(response.status_code, 200)

    def test_get_my_bookmarks(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/mybookmarks/?format=json')

        self.assertEqual(response.status_code, 200)

    def test_get_my_bookmarks_public(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/mybookmarks/?format=json&visibility=pub')

        self.assertEqual(response.status_code, 200)

    def test_get_my_bookmarks_by_tags(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/mybookmarks/?format=json&tags=python')

        self.assertEqual(response.status_code, 200)

    def test_get_bookmarks_by_text(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.get('/api/mybookmarks/?format=json&q=pyt')

        self.assertEqual(response.status_code, 200)

    def test_like_bookmark(self):
        responseLogin = self.client.post('/accounts/login/', {'login': 'user1', 'password': 'pass'})
        self.assertEqual(responseLogin.status_code, 302)
        response = self.client.put('/api/rating/1/?format=json', json.dumps({'liked': True}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.put('/api/rating/1/?format=json', json.dumps({'liked': False}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)


