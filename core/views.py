from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactUsForm
from .models import ContactUs, Rating
from countrycuzzins.models import Video
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View


class ContactUsView(FormView):
    template_name = 'core/contact_us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('country_cuzzins:home')

    def form_valid(self, form):
        if form.is_valid():
            form.check_contact_has_account(form)
            messages.success(
                self.request, f"Thank You, Your message was sent successfully! "
                )
        else:
            messages.warn(
                self.request,
                f"Oh No..., Something went wrong. Please try resending your message again."
                )
        return super().form_valid(form)


def privacyPolicy(request):
    context = {
        "website": "https://www.NoworNever.com",
    }
    return render(request, "snippets/terms_policy/privacy_policy.html", context)


class VideoRatingDetailView(View):
    model = Video
    template_name = "core/snippets/video_rating.html"
    pk_url_kwarg = "video_id"
    slug_url_kwarg = "slug"
    query_pk_and_slug = True

    def get(self, *args, **kwargs):
        context = {}
        print("Args kwargs", kwargs)
        video = Video.objects.filter(id=kwargs.get("video_id"))
        if video.exists:
            video = video.first()
            context["video"] = video
            context["ratings"] = video.rating.all()
            return context
        else:
            return render(self.request, "countrycuzzins:home")
