from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.mechanics.schemas import MechanicSchema
from app.blueprints.inventory.schemas import InventorySchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Nested(MechanicSchema, many=True)
    inventory = ma.Nested(InventorySchema, many=True)

    class Meta:
        model = ServiceTicket
        include_fk = True
