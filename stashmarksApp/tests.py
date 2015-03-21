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
