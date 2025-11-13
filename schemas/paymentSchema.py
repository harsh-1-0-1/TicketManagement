from pydantic import BaseModel
from typing import Optional

class PaymentCreateRequest(BaseModel):
    amount: int  # amount in rupees
    currency: str = "INR"
    receipt: Optional[str] = None
    user_id: Optional[int] = None    # supply if payment should be linked to a user
    ticket_id: Optional[int] = None  # supply if payment is for a ticket

class PaymentCreateResponse(BaseModel):
    id: str
    amount: int
    currency: str
    status: str

class PaymentVerifyRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str
