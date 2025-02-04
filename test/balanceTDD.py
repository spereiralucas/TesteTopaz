from app import app
from unittest import TestCase


class BalanceApiTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_1_list_successful(self):
        response = self.app.get('/api/customer/1234/10002')
        self.assertEqual(200, response.status_code)

    def test_2_not_found(self):
        response = self.app.get('/api/customer/1234/10003')
        self.assertEqual(404, response.status_code)
