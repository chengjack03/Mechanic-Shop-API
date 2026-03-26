from flask import request, jsonify
from app.extensions import db
from app.models import Customer
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
        address=data['address']
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# GET all customers
@customers_bp.route('/', methods=['GET'])
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
