from django.urls import path
from parking_details.views import *
from parking_details.mediaUploadViews import upload_media

urlpatterns = [

    path('booked_slot/<str:rpp_id>/<str:state>', SetRequestedParkingPlaceState, name="SetRequestedParkingPlaceState"),
    path('accepted_slot/<str:app_id>/verify', VerifyAcceptedSlot, name="VerifyAcceptedSlot"),

    path('details', ParkingPlaceDetails, name="ParkingPlaceDetails"),
    path('details/modify/<str:pp_id>/<str:action>', ModifyParkingPlace, name="ModifyParkingPlace"),
    path('places/image_upload', upload_media, name="upload_media"),
    path('book_slot/<str:pp_id>', BookSlot, name="BookSlot"),
    path('confirm_booking/<str:pp_id>', ConfirmBooking, name="ConfirmBooking"),
    path('get_parking/filter', GetParkingByFilter, name="GetParkingByFilter"),
    
    path('add_place', AddParkingPlace, name="add_place"),
]


