# tests/test_customers.py
from app import create_app
from app.models import db, Customer
import unittest


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer_payload = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "555-000-0000",
            "address": "123 Test St",
            "password": "testpass"
        }
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    # ── CREATE ──────────────────────────────────────────────────────────────

    def test_create_customer(self):
        response = self.client.post('/customers/', json=self.customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test User")
        self.assertEqual(response.json['email'], "test@email.com")

    def test_create_customer_missing_fields(self):
        # Negative: missing required fields
        response = self.client.post('/customers/', json={
            "name": "Bad User",
            "password": "pass"
        })
        self.assertNotEqual(response.status_code, 201)

    # ── LOGIN ───────────────────────────────────────────────────────────────

    def test_login_customer(self):
        # First create the customer, then log in
        self.client.post('/customers/', json=self.customer_payload)
        response = self.client.post('/customers/login', json={
            "email": "test@email.com",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        return response.json['token']

    def test_login_invalid_credentials(self):
        # Negative: wrong password
        self.client.post('/customers/', json=self.customer_payload)
        response = self.client.post('/customers/login', json={
            "email": "test@email.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)

    # ── GET ALL ─────────────────────────────────────────────────────────────

    def test_get_customers(self):
        self.client.post('/customers/', json=self.customer_payload)
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    # ── GET BY ID ───────────────────────────────────────────────────────────

    def test_get_customer_by_id(self):
        create_resp = self.client.post('/customers/', json=self.customer_payload)
        customer_id = create_resp.json['id']
        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], customer_id)

    def test_get_customer_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.get('/customers/99999')
        self.assertEqual(response.status_code, 404)

    # ── UPDATE ──────────────────────────────────────────────────────────────

    def test_update_customer(self):
        create_resp = self.client.post('/customers/', json=self.customer_payload)
        customer_id = create_resp.json['id']
        response = self.client.put(f'/customers/{customer_id}', json={
            "name": "Updated Name",
            "email": "test@email.com",
            "phone": "555-999-9999",
            "address": "456 New Ave"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")
        self.assertEqual(response.json['phone'], "555-999-9999")

    def test_update_customer_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.put('/customers/99999', json={
            "name": "Ghost"
        })
        self.assertEqual(response.status_code, 404)

    # ── DELETE ──────────────────────────────────────────────────────────────

    def test_delete_customer(self):
        create_resp = self.client.post('/customers/', json=self.customer_payload)
        customer_id = create_resp.json['id']
        response = self.client.delete(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_customer_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.delete('/customers/99999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
