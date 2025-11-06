from repository.ticketRepository import TicketRepository

class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    def create_ticket(self, user, title: str, description: str, price: int):
        """
        Create a new ticket with the given details. Only admin users allowed.
        """
        if user.role != "admin":
            raise PermissionError("Only admins can create tickets.")
        return self.repo.create_ticket(title, description, price)

    def list_tickets(self, skip: int = 0, limit: int = 100):
        """
        Retrieve all tickets with pagination.from repository.userRepository import 
        """
        tickets = self.repo.list_tickets(skip, limit)
        if not tickets:
            raise ValueError("No tickets found.")
        return tickets

    def delete_ticket(self,user, ticket_id: int):
        """
        Delete a ticket by ID.
        """
        if user.role != "admin":
            raise PermissionError("Only admins can delete tickets.")
        ticket = self.repo.delete_ticket(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found.")
        return ticket
