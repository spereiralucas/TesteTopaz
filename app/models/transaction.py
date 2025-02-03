from app import db
from enum import Enum
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID


class ChannelEnum(Enum):
    ATM = 0
    Teller = 1
    InternetBanking = 2
    MobileBanking = 3


class TypeEnum(Enum):
    debit = 1
    credit = 2


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    value = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    channel = db.Column(db.Integer, nullable=False)
    agency_orig = db.Column(db.Integer, nullable=False)
    account_orig = db.Column(db.Integer, nullable=False)
    agency_dest = db.Column(db.Integer, nullable=False)
    account_dest = db.Column(db.Integer, nullable=False)
