import unittest
from app import create_app
from app.extensions import db
from app.models import ServiceTicket, Customer
from datetime import datetime

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Added 'phone' here to satisfy the NOT NULL constraint
        self.customer = Customer(
            name="Test Owner", 
            email="owner@test.com", 
            phone="555-555-5555", # <--- This fixes the error
            address="123 Street", 
            password="pass"
        )
        db.session.add(self.customer)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def test_create_ticket_success(self):
        """Positive Test: Create a service ticket"""
        payload = {
            "vin": "1HGCM82633A123456",
            "service_date": "2026-03-28",
            "desc": "Brake inspection",
            "customer_id": self.customer.id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_missing_vin(self):
        """Negative Test: Fail when VIN is missing (Required for BE M2)"""
        payload = {
            "service_date": "2026-03-28",
            "customer_id": self.customer.id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_tickets_by_customer(self):
        """Test filtering tickets by customer"""
        response = self.client.get(f'/service-tickets/customer/{self.customer.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

if __name__ == '__main__':
    unittest.main()