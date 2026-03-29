from flask import request, jsonify
from . import mechanics_bp
from app.models import Mechanic, db

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    """List all mechanics"""
    mechanics = Mechanic.query.all()
    return jsonify([{"id": m.id, "name": m.name, "email": m.email} for m in mechanics]), 200

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    """Create a new mechanic"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400
        
    new_mechanic = Mechanic(name=data['name'], email=data['email'])
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify({"id": new_mechanic.id, "name": new_mechanic.name, "email": new_mechanic.email}), 201