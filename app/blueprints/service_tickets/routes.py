from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from . import service_tickets_bp
from .schemas import ServiceTicketSchema

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    new_ticket = ServiceTicket(
        vin=data['vin'],
        service_date=data['service_date'],
        desc=data['desc'],
        customer_id=data['customer_id']
    )
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = db.session.execute(db.select(ServiceTicket)).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

@service_tickets_bp.route('/<int:ticket_id>/add_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_tickets_by_customer(customer_id):
    tickets = db.session.execute(
        db.select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    ).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
