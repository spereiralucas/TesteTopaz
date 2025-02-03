from app import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    agency = db.Column(db.Integer, nullable=False)
    account = db.Column(db.Integer, nullable=False)
