from django.http import HttpResponse
from django.shortcuts import redirect, render


def authenticated_user(view_func):
    def wrapper_func(request, *args, **Kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **Kwargs)
        else:
            return redirect("/home")
            # return HttpResponse("<h1> UnAuthorized ! </h1>")

    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **Kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **Kwargs)
        else:
            return HttpResponse("<h1> UnAuthorized ! </h1>")

    return wrapper_func


