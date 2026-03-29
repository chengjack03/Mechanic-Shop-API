import unittest
from app import create_app
from app.extensions import db
from app.models import Mechanic

class TestMechanics(unittest.TestCase):
    def setUp(self):
        # Using TestingConfig to ensure isolation
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

    def test_create_mechanic_success(self):
        """Positive Test: Create a mechanic"""
        payload = {
            "name": "Mike Wrench",
            "email": "mike@shop.com",
            "phone": "555-1111",
            "salary": 60000
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Mike Wrench")

    def test_create_mechanic_missing_data(self):
        """Negative Test: Fail when salary is missing"""
        payload = {"name": "No Salary Sam", "email": "sam@shop.com"}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_mechanics_list(self):
        """Test retrieving all mechanics"""
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_mechanic(self):
        """Test updating a mechanic's information"""
        # Create one first
        m = Mechanic(name="Old Name", email="old@shop.com", phone="111", salary=50000)
        db.session.add(m)
        db.session.commit()

        response = self.client.put(f'/mechanics/{m.id}', json={"name": "New Name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "New Name")

    def test_delete_mechanic(self):
        """Test deleting a mechanic"""
        m = Mechanic(name="Gone Tomorrow", email="gone@shop.com", phone="222", salary=40000)
        db.session.add(m)
        db.session.commit()

        response = self.client.delete(f'/mechanics/{m.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.json['message'])