from app import app
from unittest import TestCase


class TransactionApiTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_1_create_transaction(self):
        dict = {
            "date_hour": "010220251120",
            "value": 30.0,
            "channel": 2,
            "origin_agency": 1234,
            "origin_account": 10001,
            "dest_agency": 1234,
            "dest_account": 10002
        }

        response = self.app.put('/api/transaction/create', json=dict)

        self.assertEqual(201, response.status_code)

    def test_2_hour_and_teller(self):
        dict = {
            "date_hour": "010220250119",
            "value": 12.03,
            "channel": 1,
            "origin_agency": 1234,
            "origin_account": 10001,
            "dest_agency": 1234,
            "dest_account": 10002
        }

        response = self.app.put('/api/transaction/create', json=dict)

        self.assertEqual(400, response.status_code)

    def test_3_hour_and_value_invalid(self):
        dict = {
            "date_hour": "010220250202",
            "value": 5927.98,
            "channel": 2,
            "origin_agency": 1234,
            "origin_account": 10001,
            "dest_agency": 1234,
            "dest_account": 10002
        }

        response = self.app.put('/api/transaction/create', json=dict)

        self.assertEqual(400, response.status_code)

    def test_4_invalid_channel_and_hour_age(self):
        dict = {
            "date_hour": "010220250535",
            "value": 760.15,
            "channel": 4,
            "origin_agency": 1234,
            "origin_account": 10001,
            "dest_agency": 1234,
            "dest_account": 10002
        }

        response = self.app.put('/api/transaction/create', json=dict)

        self.assertEqual(400, response.status_code)
