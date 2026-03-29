# tests/test_inventory.py
from app import create_app
from app.models import db
import unittest


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.part_payload = {
            "name": "Oil Filter",
            "price": 12.99
        }
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    # ── CREATE ──────────────────────────────────────────────────────────────


    def test_create_part(self):
        response = self.client.post('/inventory/', json=self.part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Oil Filter")
        self.assertEqual(response.json['price'], 12.99)

    def test_create_part_missing_fields(self):
        # Negative: missing price
        response = self.client.post('/inventory/', json={
            "name": "Broken Part"
        })
        self.assertNotEqual(response.status_code, 201)


    # ── GET ALL ─────────────────────────────────────────────────────────────


    def test_get_parts(self):
        self.client.post('/inventory/', json=self.part_payload)
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


    # ── UPDATE ──────────────────────────────────────────────────────────────


    def test_update_part(self):
        create_resp = self.client.post('/inventory/', json=self.part_payload)
        part_id = create_resp.json['id']
        response = self.client.put(f'/inventory/{part_id}', json={
            "name": "Premium Oil Filter",
            "price": 19.99
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Premium Oil Filter")
        self.assertEqual(response.json['price'], 19.99)

    def test_update_part_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.put('/inventory/99999', json={
            "name": "Ghost Part",
            "price": 0.99
        })
        self.assertEqual(response.status_code, 404)


    # ── DELETE ──────────────────────────────────────────────────────────────


    def test_delete_part(self):
        create_resp = self.client.post('/inventory/', json=self.part_payload)
        part_id = create_resp.json['id']
        response = self.client.delete(f'/inventory/{part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_part_not_found(self):
        # Negative: ID that doesn't exist
        response = self.client.delete('/inventory/99999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
