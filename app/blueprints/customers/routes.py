# app/blueprints/customers/routes.py
import datetime
import bcrypt
import jwt
from flask import request, jsonify, current_app
from app.extensions import db, limiter, cache
from app.models import Customer
from app.utils import token_required
from . import customers_bp
from .schemas import CustomerSchema

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        password=hashed.decode('utf-8')
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


@customers_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    customer = db.session.execute(
        db.select(Customer).where(Customer.email == data['email'])
    ).scalar_one_or_none()
    if not customer or not bcrypt.checkpw(data['password'].encode('utf-8'), customer.password.encode('utf-8')):
        return jsonify({"error": "Invalid email or password"}), 401
    token = jwt.encode({
        'sub': str(customer.id),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({"token": token}), 200


@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    customers = db.paginate(db.select(Customer), page=page, per_page=per_page)
    return customers_schema.jsonify(customers.items), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200


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
    if 'password' in data:
        customer.password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')
    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200
