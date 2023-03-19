from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import auth
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, datetime

import random
import uuid

from accounts.models import *
from accounts.access_decorator import *
from parking_details.models import *
from payment.views import createStripeCustomer


# global functions here


def sendUserVerificationEmail(email, name, action):

    token = createUserVerificationToken(email=email, action=action)
    print(f"token :: {token}")
    domain = "http://127.0.0.1:8000"

    if action == "signup":
        url = f"{domain}/account/verify-user/{token}"

        subject = f"Welcome to ParkMate {name} !"
        msg = f"Hey {name} ! \nComplete your signup process by activating your account."
        html_message = render_to_string('mail_template/signup.html', {"check_url": url})

    elif action == "forgotPassword":

        password_reset_url = f"{domain}/account/verify-user/{token}"

        login_token = createUserVerificationToken(email=email, action="login")
        login_url = f"{domain}/account/verify-user/{login_token}"

        subject = f"Reset your password !"
        msg = f"Hey {name} ! \nyou forgot your password No worries! Reset your password now Or directly Login."
        html_message = render_to_string('mail_template/forgotPassword.html', {"password_reset_url": password_reset_url, "login_url":login_url})

    else:
        return False

    res = send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [email, "siddhirajk77gmail.com"], html_message=html_message, fail_silently=False)
    print("res :: ", res)

    if res == 1:
        return True
    else:
        return False


def createUserVerificationToken(email, action):

    UserVerification.objects.filter(email=email, action=action).delete()

    token = f"{uuid.uuid4().hex}{uuid.uuid4().hex}"

    if UserVerification.objects.filter(token=token).exists():
        token = f"{token}{random.randint(100000000, 9999999999)}"

    new_token = UserVerification.objects.create(email=email, token=token, action=action, expire_on=(datetime.now() + timedelta(days=1)))
    new_token.save()

    return token






# Create your views here.

def testing(request):

    return render(request, "provider/providerHome.html")


@unauthenticated_user
def index(request):
    return render(request, 'landing.html')


@authenticated_user
def homepage(request):

    if request.user.user_type == "user":
        pp = ParkingPlace.objects.filter(is_active=True, in_use=False)
        data = {
            "pp": pp,
        }
        
        return render(request, 'user/homepage.html', data)
        # return HttpResponse("<h1> Homepage For User ! </h1>")

    elif request.user.user_type == "provider":

        # pp => parking_place | rpp => requested_parking_place | app =>     
        pp = ParkingTrack.objects.filter(parking_place__provider=request.user, state="parked")
        rpp = ParkingTrack.objects.filter(parking_place__provider=request.user, state="requested")
        app = ParkingTrack.objects.filter(parking_place__provider=request.user, state="accepted")

        print("rpp len :: ", len(rpp))

        data = {
            "pp": pp,
            "rpp": rpp,
            "app": app,
        }

        return render(request, 'provider/providerHome.html', data)

    return render(request, 'landing.html')



@csrf_exempt
@transaction.atomic
@unauthenticated_user
def Register(request):

    if request.method == "POST":

        rd = request.POST
        print("rd :: ", rd)

        if CustomUser.objects.filter(email=rd['email']).exists():
            return JsonResponse({"success": False,
                                 "message": {
                                    "type" : "warning",
                                    "text" : f"User with email '{rd['email']}' already exists !",
                                }})

        if not sendUserVerificationEmail(rd['email'], rd['fname'], "signup"):
            return JsonResponse({"success":False,
                                 "message": {
                                    "type" : "error",
                                    "text" : "Verification email not sent successfully!",
                                }})

        status, customer = createStripeCustomer(request.user)
        if not status:
            return JsonResponse({"success":False,
                                 "message": {
                                    "type" : "error",
                                    "text" : customer,
                                }})


        CustomUser.objects.create_user(user_type=rd['user_type'], email=rd['email'], username=rd['email'], password=rd['password'],
                                        first_name=rd['fname'], last_name=rd['lname'], mobile_number=rd['phone'], gender=rd['gender'],
                                        stripe_customer_response=customer, stripe_customer_id=customer.id)

        return JsonResponse({"success": True,
                             "message": {
                                "type" : "success",
                                "text" : "User registration successful !"
                            }})

        # return render(request, 'login_register/signup_activate.html')

    return render(request, 'login_register/signup.html')


@csrf_exempt
@transaction.atomic
@unauthenticated_user
def Login(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        user = auth.authenticate(email=rd['email'], password=rd['password'])
        print("user:",user)
        if user is not None:

            if not user.is_verified:
                return JsonResponse({"success": False,
                                     "message": {
                                        "type" : "warning",
                                        "text" : "Email is not verified. Please verify Email and try Again !"
                                     }})

            auth.login(request, user)

            return JsonResponse({"success": True,
                                 "message": {
                                    "type" : "success",
                                    "text": "User login successfully !"
                                }})

        else:
            return JsonResponse({"success": False,
                                 "message": {
                                    "type" : "error",
                                    "text" : "Oppps! Creadentials does not matched !"
                                }})

    return render(request, 'login_register/login.html')


@unauthenticated_user
def registraionSuccess(request):
    return render(request, 'login_register/verify.html')


@transaction.atomic
@unauthenticated_user
def VerifyUser(request, token):
    # deleting all expired tokens here
    UserVerification.objects.filter(expire_on__lte=datetime.now()).delete()

    token_obj = UserVerification.objects.filter(token=token, expire_on__gte=datetime.now()).first()

    if token_obj is not None:

        if token_obj.action == "signup":

            user = CustomUser.objects.filter(email=token_obj.email).first()
            user.is_verified = True
            user.email_verified_at = datetime.now()
            user.save()

            auth.login(request, user)

            token_obj.delete()
            return render(request, 'login_register/ac_activated.html')

        if token_obj.action == "login":

            user = CustomUser.objects.filter(email=token_obj.email).first()

            auth.login(request, user)

            token_obj.delete()
            return redirect("/")

        elif token_obj.action == "forgotPassword":
            token = createUserVerificationToken(email=token_obj.email, action="resetPassword")

            return render(request, 'login_register/reset_password.html', {"password_reset_token": token})


    return HttpResponse("<h1> Invalid link Or Link has been expired ! </h1>")
    # return render(request, 'login.html')


@csrf_exempt
@transaction.atomic
@unauthenticated_user
def ForgotPassword(request):

    if request.method == "POST":

        email = request.POST['email']

        user = CustomUser.objects.filter(email=email).first()

        if user is not None:
            if not sendUserVerificationEmail(email=email, name=user.first_name, action="forgotPassword"):
                return JsonResponse({"success":False,
                                     "message": {
                                        "type" : "error",
                                        "text" : "Password Reset email not sent successfully!",
                                    }})

            return JsonResponse({"success": True,
                                 "message": {
                                    "type" : "success",
                                    "text" : "Password reset email sent successfully!",
                                }})

        else:
            return JsonResponse({"success":False,
                                 "message": {
                                    "type" : "error",
                                    "text" : f"User with email '{email}' does not exists !",
                                }})


    return render(request, 'login_register/forgot_password.html')


@transaction.atomic
@unauthenticated_user
def ResetPassword(request):

    if request.method == "POST":
        print("Resetting password here !")
        UserVerification.objects.filter(expire_on__lte=datetime.now()).delete()
        rd = request.POST

        token_obj = UserVerification.objects.filter(token=rd['token'], expire_on__gte=datetime.now()).first()
        print("token :: ", token_obj)
        if token_obj is not None:

            user = CustomUser.objects.filter(email=token_obj.email).first()
            user.set_password(rd['password1'])
            user.save()

            token_obj.delete()
            UserVerification.objects.filter(email=user.email).delete()

            return render(request, 'login_register/password_reset_success.html')

    return HttpResponse("<h1> UnAuthorized ! </h1>")


def Logout(request):

    auth.logout(request)

    return HttpResponse("Logout!")
    # return render(request, '')

