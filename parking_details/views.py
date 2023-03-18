from django.http import HttpResponse
from django.shortcuts import render


from parking_details.models import *


# Create your views here.


def ParkingPlaceDetails(request, ):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        ParkingPlace.objects.create(provider=request.user, title=rd['title'], address_line_1=rd['adl1'], address_line_2=rd['adl2'],
                                    city=rd['city'], state=rd['state'], pincode=rd['pincode'], rate_per_hr=rd['rph'])

    if request.method == "PUT":
        rd = request.POST
        print("rd :: ", rd)

        ParkingPlace.objects.filter(provider=request.user, id=rd['id']).update(title=rd['title'], address_line_1=rd['adl1'], address_line_2=rd['adl2'],
                                                                                city=rd['city'], state=rd['state'], pincode=rd['pincode'], rate_per_hr=rd['rph'])

    if request.method == "DELETE":
        ParkingPlace.objects.filter(provider=request.user, id=rd['id']).delete()


    parking_places = ParkingPlace.objects.filter(provider=request.user).values('id', 'title', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'rate_per_hr', 'is_active')

    print("parking_places :: ", parking_places)

    return HttpResponse("UnAuthorized !")



def BookParkingPlace(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        pp = ParkingPlace.objects.filter(id=rd['pp_id']).first()

        new_parking_track = ParkingTrack.objects.create(user=request.user, parking_place=pp, start_time=rd['start_time'], rate_per_hr=pp.rate_per_hr,
                                                        approx_duration=rd['ad'], vehicle_type=rd['vt'], vehicle_no=rd['vn'], state="requested")


    return render(request, '')


