from django.shortcuts import redirect, render
from django.conf import settings
import stripe

from payment.models import *


# stripe api key
stripe.api_key = settings.STRIPE_SECRET_KEY


def createStripeCustomer(user):

    try:

        customer = stripe.Customer.create(
            email=user.email,
            description=user.first_name,
            name= user.first_name,
            metadata={
                "user_email":user.email,
                "user_type":user.user_type,
                "user_name": f"{user.first_name} {user.last_name}" 
            }
        )

        return True, customer

    except Exception as err:
        print("Error :: ", err)
        return False, "Error occured while creating stripe customer !"


def createStripePaymentMethod(user, pmtype, card_details={}):

    try:
        payment_method = stripe.PaymentMethod.create(
            type=pmtype,
            card=card_details,
            metadata={
                "user_email": user.email,
                "user_type": user.user_type,
                "user_name": f"{user.first_name} {user.last_name}"
            })
        
        response = stripe.PaymentMethod.attach(payment_method.id, customer=user.stripe_customer_id)

        # update customer default payment method
        args = {
            "invoice_settings":{
                'default_payment_method': payment_method.id
            }
        }

        customer = stripe.Customer.modify(user.stripe_customer_id, **args)
        user.stripe_customer_id = customer.id
        user.stripe_customer_response = customer
        user.save()

        return True, payment_method

    except Exception as err:
        print("Error :: ", err)
        return False, "Error occured while creating Stripe Payment Method !"





# Create your views here.

def PaymentView(request):

    pm = PaymentMethod.objects.filter(user=request.user).first()
    ph = PaymentHistory.objects.filter(user=request.user)

    data = {
        "pm": pm,
        "ph": ph,
    }

    if request.user == "provider":
        data['wallet'] = ProviderWallet.objects.filter(user=request.user).first()
    

    return render(request, 'payment/', data)


def AddPaymentMethod(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        pm = PaymentMethod.objects.filter(user=request.user, card_no=rd['card_no']).first()

        if pm is not None:
            return redirect("/payment/")
        
        card_details = {
            "number": rd['card_no'],
            "exp_month": rd['em'],
            "exp_year": rd['ey'],
            "cvc": rd['cvv'],
        }

        status, payment_method = createStripePaymentMethod(user=request.user, pmtype="card", card_details=card_details)
        if not status:
            return redirect("/payment/")

        PaymentMethod.objects.create(user=request.user, name_on_card=rd['noc'], ptype="card", card_no=rd['card_no'], 
                                     exp_month=rd['em'], exp_year=rd['ey'], cvv_no=rd['cvv'], billing_address=rd['ba'], currency="inr",
                                     stripe_payment_method_response=payment_method, stripe_payment_method_id=payment_method.id)


    return redirect("/payment/")



