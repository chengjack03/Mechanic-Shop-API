from app.extensions import ma
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
