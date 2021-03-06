from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import FieldDoesNotExist
from django.views.decorators.cache import never_cache
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm


def error_404(request, exception):
    return render(request, "users/HTTP/base_error.html")


def accountSignup(request):
    # Note: Need to recaptcha this form for spaming post

    context = {}
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            print("USER", user)
            login(request, user)
            messages.success(request, "Welcome %s!" % user.username)
            return HttpResponseRedirect(reverse("home"))
    context["form"] = form
    return render(request, "account/signup.html", context)


def accountLogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "account/login.html", context={"form": form})


def accountLogout(request):
    logout(request)
    messages.info(request, "You logged out successfully!")
    return HttpResponseRedirect(reverse("index"))


@login_required
def profile(request, *args, **kwargs):
    if request.method == "POST":
        u_form = RegistrationForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() or p_form.is_valid():
            if u_form.is_valid():
                u_form.save()
                messages.success(request, f"Your account has been updated!")
            if p_form.is_valid():
                p_form.save()
                messages.success(
                    request, f"Your profile image has been updated!")
            return redirect("users:user-profile")

    else:
        u_form = RegistrationForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)
