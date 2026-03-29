from flask import request, jsonify
from . import customers_bp
from app.models import Customer, db
from datetime import datetime, timezone, timedelta
import jwt
from flask import current_app

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing fields"}), 400
    
    new_customer = Customer(name=data['name'], email=data['email'], phone=data.get('phone'))
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"id": new_customer.id, "name": new_customer.name}), 201

@customers_bp.route('/login', methods=['POST'])
def login():
    # Example logic for your demo
    data = request.get_json()
    customer = Customer.query.filter_by(email=data.get('email')).first()
    if customer:
        token = jwt.encode({
            'sub': customer.id,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401