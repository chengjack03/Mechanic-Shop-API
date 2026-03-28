# app/blueprints/mechanics/routes.py
from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic
from app.utils import token_required      
from . import mechanics_bp
from .schemas import MechanicSchema
from sqlalchemy import func

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    new_mechanic = Mechanic(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        salary=data['salary']
    )
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.execute(db.select(Mechanic)).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@token_required                            # <-- NEW
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    data = request.get_json()
    mechanic.name = data.get('name', mechanic.name)
    mechanic.email = data.get('email', mechanic.email)
    mechanic.phone = data.get('phone', mechanic.phone)
    mechanic.salary = data.get('salary', mechanic.salary)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
@token_required                            # <-- NEW
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} deleted successfully"}), 200

@mechanics_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    # Join mechanics to service tickets, count tickets per mechanic, sort descending
    results = db.session.execute(
        db.select(Mechanic)
        .join(Mechanic.service_tickets)
        .group_by(Mechanic.id)
        .order_by(func.count().desc())
    ).scalars().all()

    return mechanics_schema.jsonify(results), 200