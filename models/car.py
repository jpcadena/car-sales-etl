"""
Car model for the Table
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Enum, Boolean, text, Float
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
        Enum(Gender), comment='Gender of the Buyer')
    color: str = Column(String(20), nullable=False, comment='Color of the car')
    make: str = Column(
        String(40), nullable=False, comment='Make brand of the car')
    new_car: bool = Column(
        Boolean(), default=True, nullable=False, server_default=text("true"),
        comment='True if the car is new; otherwise false')
    purchased_date: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"), comment='Date the car was purchased')
    buyer_age: Optional[int] = Column(
        Integer, comment='Age of the Buyer')
    discount: float = Column(Float, comment='Discount percentage')
    sale_price: float = Column(Float, nullable=False,
                               comment='Sale price of the car')
    created_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"), comment='Time the User was created')

    # TODO: Add constraints
    __table_args__ = (
        # CheckConstraint(settings.EMAIL_CONSTRAINT, name='email_format'),
    )
