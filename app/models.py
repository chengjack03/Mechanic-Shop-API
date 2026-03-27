# app/models.py
from .extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from typing import List


# Junction table: ServiceTicket <-> Mechanic
service_ticket_mechanic = db.Table(
    'service_ticket_mechanic',
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'), primary_key=True)
)

# Junction table: ServiceTicket <-> Inventory
service_ticket_inventory = db.Table(
    'service_ticket_inventory',
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.ForeignKey('inventory.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        secondary=service_ticket_mechanic,
        back_populates='mechanics'
    )


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[str] = mapped_column(db.Date, nullable=False)
    desc: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(
        secondary=service_ticket_mechanic,
        back_populates='service_tickets'
    )
    inventory: Mapped[List['Inventory']] = db.relationship(
        secondary=service_ticket_inventory,
        back_populates='service_tickets'
    )


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        secondary=service_ticket_inventory,
        back_populates='inventory'
    )
