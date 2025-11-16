from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    return render(request, "accounts/login.html")

def signup_view(request):
    return render(request, "accounts/signup.html")

def logout_view(request):
    logout(request)
    return redirect("home")
