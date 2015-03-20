from django.test import TestCase


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

