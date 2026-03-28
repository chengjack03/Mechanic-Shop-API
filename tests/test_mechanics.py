# tests/test_mechanics.py
from app import create_app
from app.models import db
import unittest


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic_payload = {
            "name": "Mike Wrench",
            "email": "mike@shop.com",
            "phone": "555-111-2222",
            "salary": 55000
        }
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

        # Create a customer and get a token (needed for protected routes)
        self.client.post('/customers/', json={
            "name": "Token User",
            "email": "token@email.com",
            "phone": "555-000-0001",
            "address": "1 Token St",
            "password": "tokenpass"
        })
        login_resp = self.client.post('/customers/login', json={
            "email": "token@email.com",
            "password": "tokenpass"
        })
        self.token = login_resp.json['token']
        self.auth_headers = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    # ── CREATE ──────────────────────────────────────────────────────────────


    def test_create_mechanic(self):
        response = self.client.post('/mechanics/', json=self.mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Mike Wrench")
        self.assertEqual(response.json['email'], "mike@shop.com")

    def test_create_mechanic_missing_fields(self):
        # Negative: missing required fields
        response = self.client.post('/mechanics/', json={
            "name": "Bad Mechanic"
        })
        self.assertNotEqual(response.status_code, 201)


    # ── GET ALL ─────────────────────────────────────────────────────────────


    def test_get_mechanics(self):
        self.client.post('/mechanics/', json=self.mechanic_payload)
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


    # ── GET MOST ACTIVE ─────────────────────────────────────────────────────


    def test_get_most_active_mechanics(self):
        response = self.client.get('/mechanics/most-active')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


    # ── UPDATE ──────────────────────────────────────────────────────────────


    def test_update_mechanic(self):
        create_resp = self.client.post('/mechanics/', json=self.mechanic_payload)
        mechanic_id = create_resp.json['id']
        response = self.client.put(
            f'/mechanics/{mechanic_id}',
            json={
                "name": "Updated Mike",
                "email": "mike@shop.com",
                "phone": "555-999-0000",
                "salary": 60000
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Mike")
        self.assertEqual(response.json['salary'], 60000)

    def test_update_mechanic_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.put(
            '/mechanics/99999',
            json={"name": "Ghost"},
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)


    # ── DELETE ──────────────────────────────────────────────────────────────


    def test_delete_mechanic(self):
        create_resp = self.client.post('/mechanics/', json=self.mechanic_payload)
        mechanic_id = create_resp.json['id']
        response = self.client.delete(
            f'/mechanics/{mechanic_id}',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_mechanic_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.delete(
            '/mechanics/99999',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
