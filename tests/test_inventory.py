import unittest
from app import create_app
from app.extensions import db
from app.models import Inventory # Corrected from 'Part'

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def test_create_item_success(self):
        """Positive Test: Create an inventory item"""
        payload = {"name": "Brake Pad", "price": 45.99}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake Pad")

    def test_create_item_negative(self):
        """Negative Test: Fail when price is missing"""
        payload = {"name": "No Price Part"}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_inventory(self):
        """Test retrieving the list of inventory"""
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_delete_inventory_item(self):
        """Test deleting a part"""
        item = Inventory(name="Old Bolt", price=1.99)
        db.session.add(item)
        db.session.commit()

        response = self.client.delete(f'/inventory/{item.id}')
        self.assertEqual(response.status_code, 200)