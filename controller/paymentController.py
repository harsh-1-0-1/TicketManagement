from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.paymentSchema import PaymentCreateRequest, PaymentVerifyRequest
from services.paymentServices import PaymentService

router = APIRouter()

@router.post("/create-order")
def create_order(payload: PaymentCreateRequest, db: Session = Depends(get_db)):
    return PaymentService.create_order(db, payload)

@router.post("/verify")
def verify_payment(payload: PaymentVerifyRequest, db: Session = Depends(get_db)):
    return PaymentService.verify_payment(db, payload)
