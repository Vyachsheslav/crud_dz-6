from unittest import TestCase
from rest_framework.test import APIClient


class TestS(TestCase):
    def test_samle_view(self):
        client = APIClient()
        response = client.get('/api/v1/test/')
        self.assertEqual(response.status_code, 200)
