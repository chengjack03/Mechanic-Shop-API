from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from . import inventory_bp
from .schemas import InventorySchema

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


@inventory_bp.route('/', methods=['POST'])
def create_part():
    data = request.get_json()
    new_part = Inventory(name=data['name'], price=data['price'])
    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201


@inventory_bp.route('/', methods=['GET'])
def get_parts():
    parts = db.session.execute(db.select(Inventory)).scalars().all()
    return inventories_schema.jsonify(parts), 200


@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    data = request.get_json()
    part.name = data.get('name', part.name)
    part.price = data.get('price', part.price)
    db.session.commit()
    return inventory_schema.jsonify(part), 200


@inventory_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {part_id} deleted"}), 200
