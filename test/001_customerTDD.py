from app import app
from unittest import TestCase


class CustomerApiTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_1_create_customer(self):
        dict = {
            "name": "Fulano",
            "age": 60
        }

        response = self.app.put('/api/customer/1234/10001', json=dict)
        self.assertEqual(201, response.status_code)

        customer_2 = {
            "name": "Beltrano",
            "age": 45
        }

        response_2 = self.app.put('/api/customer/1234/10002', json=customer_2)
        self.assertEqual(201, response_2.status_code)

    def test_2_duplicate_customer(self):
        dict = {
            "name": "Fulano",
            "age": 60
        }

        response = self.app.put('/api/customer/1234/10001', json=dict)

        self.assertEqual(409, response.status_code)

    def test_3_missing_field(self):
        dict = {
            "name": "Beltrano"
        }

        response = self.app.put('/api/customer/1234/10002', json=dict)

        self.assertEqual(400, response.status_code)

    def test_4_invalid_param(self):
        dict = {
            "name": "Beltrano",
            "teste": "teste"
        }

        response = self.app.put('/api/customer/1234/10002', json=dict)

        self.assertEqual(400, response.status_code)

    def test_5_invalid_param_type(self):
        dict = {
            "name": "Beltrano",
            "age": "string"
        }

        response = self.app.put('/api/customer/1234/10002', json=dict)

        self.assertEqual(400, response.status_code)

    def test_6_null_param(self):
        dict = {
            "name": "Beltrano",
            "age": None
        }

        response = self.app.put('/api/customer/1234/10002', json=dict)

        self.assertEqual(400, response.status_code)
