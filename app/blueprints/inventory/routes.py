from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from . import inventory_bp
from .schemas import InventorySchema

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

@inventory_bp.route('/', methods=['POST'])
def create_part():
    """
    Create a new inventory part
    ---
    tags:
      - Inventory
    parameters:
      - in: body
        name: body
        schema:
          id: InventoryPayload
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: "Brake Pad"
            price:
              type: number
              example: 45.99
    responses:
      201:
        description: Part created successfully
      400:
        description: Missing required fields
    """
    data = request.get_json()
    
    # VALIDATION FIX: Check if fields exist to prevent KeyError
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing name or price"}), 400

    new_part = Inventory(name=data['name'], price=data['price'])
    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201

@inventory_bp.route('/', methods=['GET'])
def get_parts():
    """
    Get all inventory parts
    ---
    tags:
      - Inventory
    responses:
      200:
        description: A list of inventory parts
    """
    parts = db.session.execute(db.select(Inventory)).scalars().all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    """
    Update an existing part
    ---
    tags:
      - Inventory
    parameters:
      - name: part_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/InventoryPayload'
    responses:
      200:
        description: Part updated
      404:
        description: Part not found
    """
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
    """
    Delete a part from inventory
    ---
    tags:
      - Inventory
    parameters:
      - name: part_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Part deleted
      404:
        description: Part not found
    """
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {part_id} deleted"}), 200