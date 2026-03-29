from flask import request, jsonify
from . import customers_bp
from app.models import Customer, db
from datetime import datetime, timezone, timedelta
import jwt
from flask import current_app

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    # Check for all fields required by your model/test
    required = ['name', 'email', 'password', 'address']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_customer = Customer(
        name=data['name'], 
        email=data['email'], 
        password=data['password'], # In a real app, hash this!
        address=data['address'],
        phone=data.get('phone', "")
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"id": new_customer.id, "name": new_customer.name, "email": new_customer.email}), 201

@customers_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email} for c in customers]), 200

@customers_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    customer = Customer.query.filter_by(email=data.get('email')).first()
    if customer and customer.password == data.get('password'):
        token = jwt.encode({
            'sub': customer.id,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@customers_bp.route('/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'GET':
        return jsonify({"id": customer.id, "name": customer.name, "email": customer.email}), 200
    
    if request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200

    # PUT Logic
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)
    db.session.commit()
    return jsonify({"id": customer.id, "name": customer.name, "phone": customer.phone}), 200