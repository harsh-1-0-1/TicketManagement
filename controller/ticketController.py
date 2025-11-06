from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from repository.ticketRepository import TicketRepository
from services.ticketServices import TicketService
from schemas.ticketSchema import TicketSchema ,TicketCreate,TicketDelete# Your ticket schemas module
from utils.dependencies import get_current_user  # Your auth dependency returning user


router = APIRouter()

# Dependency factory for TicketService
def get_ticket_service(db: Session = Depends(get_db)) -> TicketService:
    repo = TicketRepository(db)
    return TicketService(repo)


@router.post("/create", response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    service: TicketService = Depends(get_ticket_service),
    current_user = Depends(get_current_user)
):
    """
    Admin-only endpoint to create a ticket.
    """
    try:
        ticket = service.create_ticket(
            user=current_user,
            title=ticket_in.title,
            description=ticket_in.description,
            price=ticket_in.price
        )
        return ticket
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.get("/", response_model=List[TicketSchema])
def list_tickets(
    skip: int = 0,
    limit: int = 100,
    service: TicketService = Depends(get_ticket_service)
):
    """
    List tickets (accessible by any user).
    """
    try:
        tickets = service.list_tickets(skip=skip, limit=limit)
        return tickets
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{ticket_id}", response_model=TicketSchema)
def delete_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
    current_user = Depends(get_current_user)
):
    """
    Admin-only endpoint to delete a ticket by ID.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete tickets.")
    
    try:
        deleted = service.delete_ticket(ticket_id)
        return deleted
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
