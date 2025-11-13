from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum
Base = declarative_base()


class PaymentStatus(PyEnum):
    created = "created"
    paid = "paid"
    failed = "failed"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(5), default="INR", nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, currency='{self.currency}', status='{self.status}')>"
