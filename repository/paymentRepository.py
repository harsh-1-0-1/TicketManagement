from sqlalchemy.orm import Session
from models.paymentModel import Payment

class PaymentRepository:
    @staticmethod
    def create_payment(db: Session, order_id: str, amount: int, currency: str, status: str, user_id: int = None, ticket_id: int = None):
        payment = Payment(order_id=order_id, amount=amount, currency=currency, status=status, user_id=user_id, ticket_id=ticket_id)
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

    @staticmethod
    def get_by_order_id(db: Session, order_id: str):
        return db.query(Payment).filter(Payment.order_id == order_id).first()
