from sqlalchemy.orm import Session
from models.paymentModel import Payment  # assume you have a Payment model

class PaymentRepository:
    @staticmethod
    def create_payment(db: Session, order_id: str, amount: int, currency: str, status: str):
        payment = Payment(order_id=order_id, amount=amount, currency=currency, status=status)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def update_payment_status(db: Session, order_id: str, status: str):
        payment = db.query(Payment).filter(Payment.order_id == order_id).first()
        if payment:
            payment.status = status
            db.commit()
            db.refresh(payment)
        return payment
