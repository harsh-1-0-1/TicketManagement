# models/ticketModel.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)

    # payments made for this ticket
    payments = relationship("Payment", back_populates="ticket", cascade="all, delete-orphan")
