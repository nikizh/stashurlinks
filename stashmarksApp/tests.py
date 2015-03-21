from django.test import TestCase
from django.contrib.auth.models import User
import stashmarksApp.models as models

class ModelTests(TestCase):

    def test_ensure_tag_constructor(self):
        tag = models.Tag(name="Test")
        tag.save()
        self.assertEqual(tag.name, "Test")

    def test_ensure_bookmark_constructor(self):
        testUser = User()
        testUser.save()
        bm = models.Bookmark(title="Test",public=False, likes=1, owner=testUser)
        bm.save()
        self.assertEqual(bm.title, "Test")
        self.assertEqual(bm.public, False)
        self.assertEqual(bm.likes, 1)
        self.assertEqual(bm.owner,testUser)

    def test_ensure_ratings_constructor(self):
        testUser = User()
        testUser.save()
        bm = models.Bookmark(title="Test",public=False, likes=1, owner=testUser)
        bm.save()
        rating = models.Ratings(owner=testUser,bookmark=bm,liked=True)
        rating.save()
        self.assertEqual(rating.owner,testUser)
        self.assertEqual(rating.bookmark,bm)
        self.assertEqual(rating.liked,True)

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

