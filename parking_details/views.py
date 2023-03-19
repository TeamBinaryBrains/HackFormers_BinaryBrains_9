import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from datetime import datetime
from parking_details.models import *


# Create your views here.

def AddParkingPlace(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        url_list = [
            "http://127.0.0.1:8000/media/parking_places/image/209307f3ef8f4544ae5f09bbce876591.jpeg",
            "http://127.0.0.1:8000/media/parking_places/image/ac667c4cd2954905ba3072de6c7dbde7.jpeg",
            "http://127.0.0.1:8000/media/parking_places/image/81d420bbf0b14394b88c62fe81022c48.jpeg",
        ]

        ParkingPlace.objects.create(provider=request.user, title=rd['title'], address_line_1=rd['adl1'], address_line_2=rd['adl2'],
                                    city=rd['city'], state=rd['state'], pincode=rd['pincode'], rate_per_hr=rd['rph'], place_images=url_list)

        parking_places = ParkingPlace.objects.filter(provider=request.user)

        print("parking_places :: ", parking_places)

        data = {
            "pp": parking_places,
        }

        return render(request, 'provider/parking_detail.html', data)

    return render(request, 'provider/add_place.html')


def ParkingPlaceDetails(request):

    parking_places = ParkingPlace.objects.filter(provider=request.user)

    print("parking_places :: ", parking_places)

    data = {
        "pp": parking_places,
    }

    return render(request, 'provider/parking_detail.html', data)
    # return HttpResponse("UnAuthorized !")


def ModifyParkingPlace(request, pp_id, action):

    if action == "edit":
        pass
        # rd = request.POST
        # print("rd :: ", rd)

        # ParkingPlace.objects.filter(provider=request.user, id=rd['id']).update(title=rd['title'], address_line_1=rd['adl1'], address_line_2=rd['adl2'],
        #                                                                         city=rd['city'], state=rd['state'], pincode=rd['pincode'], rate_per_hr=rd['rph'])

    if action == "delete":
        ParkingPlace.objects.filter(provider=request.user, id=pp_id).delete()


    return redirect("/parking/details")


def BookParkingPlace(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        pp = ParkingPlace.objects.filter(id=rd['pp_id']).first()

        new_parking_track = ParkingTrack.objects.create(user=request.user, parking_place=pp, start_time=rd['start_time'], rate_per_hr=pp.rate_per_hr,
                                                        approx_duration=rd['ad'], vehicle_type=rd['vt'], vehicle_no=rd['vn'], state="requested")


    return render(request, '')


def SetRequestedParkingPlaceState(request, rpp_id, state):

    if request.method == "POST":
        ParkingTrack.objects.filter(parking_place__provider=request.user, id=rpp_id, state="requested").update(state=state)

    return redirect("/")


def VerifyAcceptedSlot(request, app_id):

    if request.method == "POST":
        app_obj = ParkingTrack.objects.filter(parking_place__provider=request.user, id=app_id, state="accepted").first()
        
        if request.POST['verify_otp'] == app_obj.verify_otp:
            app_obj.state = "parked"
            app_obj.save()

    return redirect("/")


def BookSlot(request, pp_id):

    pp = ParkingPlace.objects.filter(id=pp_id).first()

    if pp is not None:
        data = {
            "pp": pp,
        }
        return render(request, 'user/booking.html', data)
        
    return redirect("/payment/")


def ConfirmBooking(request, pp_id):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)
        pp = ParkingPlace.objects.filter(id=pp_id).first()
        verify_otp = random.randint(10000, 99999)
        ParkingTrack.objects.create(user=request.user, parking_place=pp, start_time=datetime.now(), rate_per_hr=pp.rate_per_hr,
                                    approx_duration=rd['ad'], vehicle_type=rd['vt'], vehicle_no=rd['vn'], state="requested",
                                    verify_otp=verify_otp)
        
        pp.in_use = True
        pp.save()

        # return HttpResponse(f"Your Booking successful! OTP :: {verify_otp}")
        return render(request, 'user/otp.html', {"verify_otp":verify_otp})

    return redirect("/")



def GetParkingByFilter(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        fpp = ParkingPlace.objects.filter((Q(address_line_1__icontains=rd['street']) | Q(address_line_2__icontains=rd['street'])), state__icontains=rd['state'], city__icontains=rd['city'])
        
        print("\nfpp :: ", fpp)
        data = {
            "pp": fpp,
        }

        return render(request, 'user/homepage.html', data)

    return redirect("/")



