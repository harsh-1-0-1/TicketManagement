from fastapi import HTTPException, status
import razorpay
from utils.razorpayClient import razorpay_client
from repository.paymentRepository import PaymentRepository
from schemas.paymentSchema import PaymentCreateRequest, PaymentVerifyRequest

class PaymentService:
    @staticmethod
    def create_order(db, payload: PaymentCreateRequest):
        try:
            # Convert to paise (Razorpay requires paise)
            amount_in_paise = payload.amount * 100

            order = razorpay_client.order.create({
                "amount": amount_in_paise,
                "currency": payload.currency,
                "receipt": payload.receipt or "receipt#1",
                "payment_capture": 1
            })

            # Save order in DB
            PaymentRepository.create_payment(
                db=db,
                order_id=order["id"],
                amount=payload.amount,
                currency=payload.currency,
                status=order["status"]
            )

            return order
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create Razorpay order: {str(e)}"
            )

    @staticmethod
    def verify_payment(db, payload: PaymentVerifyRequest):
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': payload.order_id,
                'razorpay_payment_id': payload.payment_id,
                'razorpay_signature': payload.signature
            })

            # Update status to "paid"
            PaymentRepository.update_payment_status(db, payload.order_id, "paid")
            return {"message": "Payment verified successfully"}
        except razorpay.errors.SignatureVerificationError:
            PaymentRepository.update_payment_status(db, payload.order_id, "failed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed (invalid signature)"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment verification failed: {str(e)}"
            )
