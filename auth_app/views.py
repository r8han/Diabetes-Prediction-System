from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from diabetes_prediction_system.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from random import randrange


def user_signup(request):
    if request.method == "POST":
        un = request.POST.get("un")
        try:
            usr = User.objects.get(username=un)
            context = {
                "error": True,
                "error_msg": "Email already registered"
            }
            return render(request, "auth_app/user_signup.html", context)
        except User.DoesNotExist:
            pw = ""
            text = "abcdefghijklmnopqrstuvwxyz"
            for i in range(5):
                pw = pw + text[randrange(len(text))]

            sub = "Diabetes Prediction System"
            msg = "Your Password is " + str(pw)
            sender = EMAIL_HOST_USER
            receiver = [str(un)]
            send_mail(sub, msg, sender, receiver)

            usr = User.objects.create_user(username=un, password=pw)
            usr.save()
            return redirect("login")
    else:
        return render(request, "auth_app/user_signup.html")


def user_login(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        usr = authenticate(username=un, password=pw)
        if usr is None:
            context = {
                "error": True,
                "error_msg": "Check Credentials"
            }
            return render(request, "auth_app/user_login.html", context)
        else:
            login(request, usr)
            return redirect("home")
    else:
        return render(request, "auth_app/user_login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def user_np(request):
    if request.method == "POST":
        un = request.POST.get("un")
        try:
            usr = User.objects.get(username=un)
            pw = ""
            text = "abcdefghijklmnopqrstuvwxyz"
            for i in range(5):
                pw = pw + text[randrange(len(text))]
            print(pw)

            sub = "Diabetes Prediction System"
            msg = "Your New Password is " + str(pw)
            sender = EMAIL_HOST_USER
            receiver = [str(un)]
            send_mail(sub, msg, sender, receiver)

            usr.set_password(pw)
            usr.save()
            return redirect("login")

        except User.DoesNotExist:
            context = {
                "error": True,
                "error_msg": "Email not registered"
            }
            return render(request, "auth_app/user_np.html", context)
    else:
        return render(request, "auth_app/user_np.html")
