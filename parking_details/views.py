from django.http import HttpResponse
from django.shortcuts import redirect, render
from parking_details.models import *


# Create your views here.


def ParkingPlaceDetails(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        ParkingPlace.objects.create(provider=request.user, title=rd['title'], address_line_1=rd['adl1'], address_line_2=rd['adl2'],
                                    city=rd['city'], state=rd['state'], pincode=rd['pincode'], rate_per_hr=rd['rph'])

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






