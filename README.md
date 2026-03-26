# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask, SQLAlchemy, and MySQL.

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create MySQL database: `CREATE DATABASE mechanic_shop_db;`
6. Update `config.py` with your MySQL password
7. Run the app: `python app.py`

## Endpoints

### Customers
- POST `/customers/` - Create a customer
- GET `/customers/` - Get all customers
- PUT `/customers/<id>` - Update a customer
- DELETE `/customers/<id>` - Delete a customer

### Mechanics
- POST `/mechanics/` - Create a mechanic
- GET `/mechanics/` - Get all mechanics
- PUT `/mechanics/<id>` - Update a mechanic
- DELETE `/mechanics/<id>` - Delete a mechanic

### Service Tickets
- POST `/service-tickets/` - Create a service ticket
- GET `/service-tickets/` - Get all service tickets
- PUT `/service-tickets/<ticket_id>/add_mechanic/<mechanic_id>` - Assign mechanic
- PUT `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic
- GET `/service-tickets/customer/ustomer_id>` - Get tickets by customer
