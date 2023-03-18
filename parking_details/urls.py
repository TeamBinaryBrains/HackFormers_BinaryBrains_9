from django.urls import path
from parking_details.views import *


urlpatterns = [

    path('booked_slot/<str:rpp_id>/<str:state>', SetRequestedParkingPlaceState, name="SetRequestedParkingPlaceState"),
    path('accepted_slot/<str:app_id>/verify', VerifyAcceptedSlot, name="VerifyAcceptedSlot"),
    
]


