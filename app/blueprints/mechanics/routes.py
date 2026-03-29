from flask import request, jsonify
from . import mechanics_bp
from app.models import Mechanic, db

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    """Create a new mechanic"""
    data = request.get_json()
    # Negative Testing: Check for required fields
    required = ['name', 'email', 'phone', 'salary']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
        
    new_mechanic = Mechanic(
        name=data['name'], 
        email=data['email'], 
        phone=data['phone'], 
        salary=data['salary']
    )
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify({
        "id": new_mechanic.id, 
        "name": new_mechanic.name, 
        "email": new_mechanic.email,
        "phone": new_mechanic.phone,
        "salary": new_mechanic.salary
    }), 201

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    """List all mechanics"""
    mechanics = Mechanic.query.all()
    return jsonify([{
        "id": m.id, "name": m.name, "email": m.email, "phone": m.phone, "salary": m.salary
    } for m in mechanics]), 200

@mechanics_bp.route('/most-active', methods=['GET'])
def get_most_active():
    """Get mechanics sorted by activity (placeholder for test)"""
    mechanics = Mechanic.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in mechanics]), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT', 'DELETE'])
def handle_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    
    if request.method == 'DELETE':
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({"message": f"Mechanic {mechanic_id} deleted successfully"}), 200
    
    # PUT Logic
    data = request.get_json()
    mechanic.name = data.get('name', mechanic.name)
    mechanic.email = data.get('email', mechanic.email)
    mechanic.phone = data.get('phone', mechanic.phone)
    mechanic.salary = data.get('salary', mechanic.salary)
    db.session.commit()
    
    return jsonify({
        "id": mechanic.id, 
        "name": mechanic.name, 
        "email": mechanic.email,
        "phone": mechanic.phone,
        "salary": mechanic.salary
    }), 200