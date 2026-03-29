# tests/test_service_tickets.py
from app import create_app
from app.models import db
import unittest


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

        # Create a customer to use as ticket owner
        create_resp = self.client.post('/customers/', json={
            "name": "Ticket Owner",
            "email": "owner@email.com",
            "phone": "555-000-0002",
            "address": "2 Owner St",
            "password": "ownerpass"
        })
        self.customer_id = create_resp.json['id']

        self.ticket_payload = {
            "vin": "1HGCM82633A123456",
            "service_date": "2025-01-15",
            "desc": "Oil change and tire rotation",
            "customer_id": self.customer_id
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    # ── CREATE ──────────────────────────────────────────────────────────────


    def test_create_ticket(self):
        response = self.client.post('/service-tickets/', json=self.ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "1HGCM82633A123456")
        self.assertEqual(response.json['customer_id'], self.customer_id)

    def test_create_ticket_missing_fields(self):
        # Negative: missing required fields
        response = self.client.post('/service-tickets/', json={
            "vin": "1HGCM82633A999999"
        })
        self.assertNotEqual(response.status_code, 201)


    # ── GET ALL ─────────────────────────────────────────────────────────────


    def test_get_tickets(self):
        self.client.post('/service-tickets/', json=self.ticket_payload)
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


    # ── GET BY CUSTOMER ──────────────────────────────────────────────────────


    def test_get_tickets_by_customer(self):
        self.client.post('/service-tickets/', json=self.ticket_payload)
        response = self.client.get(f'/service-tickets/customer/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]['customer_id'], self.customer_id)

    def test_get_tickets_by_customer_no_tickets(self):
        # Negative: customer with no tickets returns empty list
        response = self.client.get('/service-tickets/customer/99999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


    # ── EDIT MECHANICS ON TICKET ─────────────────────────────────────────────


    def test_edit_ticket_mechanics(self):
        ticket_resp = self.client.post('/service-tickets/', json=self.ticket_payload)
        ticket_id = ticket_resp.json['id']
        mechanic_resp = self.client.post('/mechanics/', json={
            "name": "Test Mechanic",
            "email": "mech@shop.com",
            "phone": "555-333-4444",
            "salary": 50000
        })
        mechanic_id = mechanic_resp.json['id']
        response = self.client.put(
            f'/service-tickets/{ticket_id}/edit',
            json={"add_ids": [mechanic_id], "remove_ids": []}
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_not_found(self):
        # Negative: ticket ID that doesn't exist
        response = self.client.put(
            '/service-tickets/99999/edit',
            json={"add_ids": [], "remove_ids": []}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
