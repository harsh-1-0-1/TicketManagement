from pydantic import BaseModel

class PaymentCreateRequest(BaseModel):
    amount: int  # amount in rupees
    currency: str = "INR"
    receipt: str | None = None

class PaymentCreateResponse(BaseModel):
    id: str
    amount: int
    currency: str
    status: str

class PaymentVerifyRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str
