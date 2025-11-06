from sqlalchemy.orm import Session
from models.ticketModel import TicketModel

class TicketRepository:
    """
    Handles all direct database operations related to the Ticket model.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_ticket(self, title: str, description: str, price: int):
        """
        Create and persist a new ticket in the database.
        """
        ticket = TicketModel(
            title=title,
            description=description,
            price=price
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def list_tickets(self, skip: int = 0, limit: int = 100):
        """
        Return a paginated list of tickets.
        """
        return self.db.query(TicketModel).offset(skip).limit(limit).all()

    def delete_ticket(self, ticket_id: int):
        """
        Delete a ticket by ID.
        """
        ticket = self.db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if ticket:
            self.db.delete(ticket)
            self.db.commit()
        return ticket