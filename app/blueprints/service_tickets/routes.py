from flask import request, jsonify
from . import service_tickets_bp
from app.models import ServiceTicket, db
from datetime import datetime

@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    """
    Create a new service ticket
    ---
    tags: [Service Tickets]
    parameters:
      - in: body
        name: body
        schema:
          required: [vin, service_date, desc, customer_id]
          properties:
            vin: {type: string, example: "1HGCM82633A123456"}
            service_date: {type: string, example: "2025-01-15"}
            desc: {type: string, example: "Full engine diagnostic"}
            customer_id: {type: integer, example: 1}
    responses:
      201: {description: "Ticket created"}
      400: {description: "Invalid input"}
    """
    data = request.get_json()
    required = ['vin', 'service_date', 'desc', 'customer_id']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        formatted_date = datetime.strptime(data['service_date'], '%Y-%m-%d').date()
        new_ticket = ServiceTicket(
            vin=data['vin'],
            service_date=formatted_date,
            desc=data['desc'],
            customer_id=data['customer_id']
        )
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify({
            "id": new_ticket.id,
            "vin": new_ticket.vin,
            "service_date": new_ticket.service_date.strftime('%Y-%m-%d'),
            "desc": new_ticket.desc,
            "customer_id": new_ticket.customer_id
        }), 201
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

@service_tickets_bp.route('/', methods=['GET'])
def get_tickets():
    """Get all service tickets"""
    tickets = ServiceTicket.query.all()
    return jsonify([{
        "id": t.id, "vin": t.vin, 
        "service_date": t.service_date.strftime('%Y-%m-%d'),
        "desc": t.desc, "customer_id": t.customer_id
    } for t in tickets]), 200

@service_tickets_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_tickets_by_customer(customer_id):
    """Get tickets for a specific customer"""
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([{
        "id": t.id, "vin": t.vin, 
        "service_date": t.service_date.strftime('%Y-%m-%d'),
        "customer_id": t.customer_id, "desc": t.desc
    } for t in tickets]), 200

@service_tickets_bp.route('/<int:ticket_id>/add_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic_to_ticket(ticket_id, mechanic_id):
    """Assign a mechanic to a ticket"""
    from app.models import Mechanic
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify({"id": ticket.id, "message": "Mechanic added"}), 200