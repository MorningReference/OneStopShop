from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

import bcrypt


def index(request):
    return render(request, "index.html")


def new_user(request):
    context = {
        "all_users": User.objects.all(),
    }
    return render(request, "register.html", context)


def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        add_user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=pw_hash,
        )
        request.session["userid"] = add_user.id
        messages.info(request, "Successfully Registered")
    return redirect("/dashboard")


def user_login(request):
    user = User.objects.filter(email=request.POST["email"])
    if len(user) == 0:
        messages.error(request, "Please check your email and password")
        return redirect("/")
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(),
            logged_user.password.encode()
        ):
            request.session["userid"] = logged_user.id
            messages.info(request, "Successfully Logged In")
            return redirect(f"/dashboard")

    # if made it this far and password incorrect:
    messages.error(request, "Please check your email and password")
    return redirect("/")


def success(request):
    context = {
        "current_user": User.objects.get(id=request.session["userid"])
    }
    return render(request, "success.html", context)


def logout(request):
    request.session.flush()
    messages.info(
        request, "Congratulations, You have logged out successfully!")
    return redirect("/")
