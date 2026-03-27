from flask import request, jsonify
from app.extensions import db, limiter, cache
from app.models import Customer
from app.utils import encode_token, token_required
from . import customers_bp
from .schemas import CustomerSchema


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# CREATE a customer
@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        password=data['password']  # <-- added here
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# GET all customers
@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_customers():
    customers = db.session.execute(db.select(Customer)).scalars().all()
    return customers_schema.jsonify(customers), 200

# UPDATE a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# DELETE a customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200




@customers_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    customer = db.session.execute(
        db.select(Customer).where(Customer.email == data['email'])
    ).scalar_one_or_none()

    if not customer or customer.password != data['password']:
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token}), 200


# GET tickets for logged-in customer (token protected)
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets():
    from app.models import ServiceTicket
    tickets = db.session.execute(
        db.select(ServiceTicket).where(ServiceTicket.customer_id == request.customer_id)
    ).scalars().all()

    from app.blueprints.service_tickets.schemas import ServiceTicketSchema
    tickets_schema = ServiceTicketSchema(many=True)
    return tickets_schema.jsonify(tickets), 200
