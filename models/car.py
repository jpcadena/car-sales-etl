"""
Car model for the Table
"""
from datetime import datetime
from typing import Optional

from numpy import uint8, uint16
from sqlalchemy import Column, Integer, String, Enum, Boolean, text, Float, \
    CheckConstraint, SmallInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP

from core.config import settings
from db.base import Base
from schema.gender import Gender


class Car(Base):
    """
    Car class as a table model
    """
    __tablename__ = 'car'

    id: int = Column(
        Integer, index=True, unique=True, nullable=False, primary_key=True,
        comment='ID of the car sale')
    buyer_gender: Optional[Gender] = Column(
        Enum(Gender), nullable=True, comment='Gender of the Buyer')
    color: str = Column(
        String(20), CheckConstraint('char_length(color) >= 3'),
        nullable=False, comment='Color of the car')
    new_car: bool = Column(
        Boolean(), default=True, nullable=False, server_default=text("true"),
        comment='True if the car is new; otherwise false')
    purchase_date: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        nullable=False, comment='Date the car was purchased')
    buyer_age: Optional[uint8] = Column(
        SmallInteger, CheckConstraint('buyer_age >= 18'), nullable=True,
        comment='Age of the Buyer')
    discount: Optional[float] = Column(
        Float(2), nullable=True, comment='Discount percentage')
    sale_price: float = Column(
        Float(2), nullable=False, comment='Sale price of the car')
    purchase_year: uint16 = Column(
        SmallInteger, CheckConstraint(
            f'purchase_year >= 0 and purchase_year <= {settings.CURRENT_YEAR}'
        ), nullable=False, comment='Year the car was purchased')
    make_classification: str = Column(
        SmallInteger, CheckConstraint('make_classification >= 1'),
        nullable=False, comment='Make brand of the car categorized by numbers')
    created_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"), comment='Time the User was created')
