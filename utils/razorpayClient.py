from decouple import config
import razorpay


razorpay_client = razorpay.Client(auth=(
    config("RAZORPAY_KEY_ID"),
    config("RAZORPAY_KEY_SECRET")
))
print("Razorpay Client Initialized:", razorpay_client)