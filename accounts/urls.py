from django.urls import path
from accounts.views import *


urlpatterns = [

    path('register', Register, name="register"),
    path('login', Login, name="login"),
    path('logout', Logout, name="logout"),
    path('forgot-password', ForgotPassword, name="forgot-password"),
    path('verify-user/<str:token>', VerifyUser, name="verify-user"),
    path('reset-password', ResetPassword, name="reset-password"),
    
    path('registraion-success', registraionSuccess, name="registraion-success"),
    path('forgot-password-success', registraionSuccess, name="registraion-success"),
]

