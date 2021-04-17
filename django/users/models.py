import os
import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from countrycuzzins.models import Video


from django.urls import reverse, reverse_lazy
MEDIA_ROOT = "static" + settings.MEDIA_ROOT



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(  upload_to="images/profile/")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def getImage(self):
        return "static/media/images/profile/default_profile.png"


    def get_absolute_url(self):
        return reverse("users:user-profile",
                       kwargs={"user": self.user.username})


class NewsLetter(models.Model):
    email = models.EmailField(
        max_length=100, unique=True, blank=False, null=True)
    has_account = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return (
            f"{ self.email}  | account {self.check_for_account}",
            f"| subscribed {created}",
        )

