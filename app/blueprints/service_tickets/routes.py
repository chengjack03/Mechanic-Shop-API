from flask import request, jsonify
from . import service_tickets_bp
from app.models import ServiceTicket, Customer, db
from datetime import datetime

@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    # Logic for the "Negative Test" (Missing fields)
    required = ['vin', 'service_date', 'desc', 'customer_id']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_ticket = ServiceTicket(
            vin=data['vin'],
            # Ensures date is formatted correctly for the DB
            service_date=datetime.strptime(data['service_date'], '%Y-%m-%d').date(),
            desc=data['desc'],
            customer_id=data['customer_id']
        )
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify({
            "id": new_ticket.id,
            "vin": new_ticket.vin,
            "customer_id": new_ticket.customer_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@service_tickets_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify([{"id": t.id, "vin": t.vin, "customer_id": t.customer_id} for t in tickets]), 200

@service_tickets_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_by_customer(customer_id):
    # Test expects a list (even if empty) for this endpoint
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([{"id": t.id, "vin": t.vin, "customer_id": t.customer_id} for t in tickets]), 200