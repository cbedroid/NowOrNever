from django.contrib import messages
from ipware import get_client_ip
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import FieldDoesNotExist
from django.views.decorators.cache import never_cache
from .forms import ContactUsForm
from .models import ContactUs


@never_cache
def contactUs(request):
    if request.method == "POST":
        c_form = ContactUsForm(request.POST)
        if c_form.is_valid():
            c_form.save(commit=True)
            print('\nDIR C_FORM', dir(c_form))
            print('Post C_FORM', c_form)
            client_ip, is_routable = get_client_ip(request,)
            if client_ip is None:
                print('IP Address not available')
            else:
                print('Client IP', client_ip,)
                try:
                    ContactUs.objects.update(pk=c_form, defaults={
                                             "ip_address": client_ip})
                except FieldDoesNotExist as e:
                    print('Updating Field Failed', e)

            messages.success(
                request, f"Thank You, Your message was sent successfully! "
            )
            return HttpResponseRedirect(reverse("home"))
            # return redirect("home")
        else:
            print('Form not validate')
            return redirect("contact_us")
    else:
        c_form = ContactUsForm()

    context = {"form": c_form}
    return render(request, "users/contact_us.html", context)


def privacyPolicy(request):
    context = {
        "website": "https://www.NoworNever.com",
    }
    return render(request, "snippets/terms_policy/privacy_policy.html", context)
