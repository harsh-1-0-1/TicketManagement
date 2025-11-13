# models/paymentModel.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum
from database import Base   # use the shared Base

class PaymentStatus(PyEnum):
    created = "created"
    paid = "paid"
    failed = "failed"

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(128), unique=True, index=True, nullable=False)   # razorpay order id
    amount = Column(Float, nullable=False)
    currency = Column(String(5), default="INR", nullable=False)
    status = Column(String(20), nullable=False, default=PaymentStatus.created.value)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # relations
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)

    user = relationship("User", back_populates="payments")
    ticket = relationship("TicketModel", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, amount={self.amount}, status={self.status})>"
