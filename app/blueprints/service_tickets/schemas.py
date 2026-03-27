# app/blueprints/service_tickets/schemas.py
from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.mechanics.schemas import MechanicSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Nested(MechanicSchema, many=True)

    class Meta:
        model = ServiceTicket
        include_fk = True
