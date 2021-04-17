from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ContactUs(models.Model):
    firstname = models.CharField(max_length=60, blank=False, null=True)
    lastname = models.CharField(max_length=60, blank=False, null=True)
    #ip_address = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, blank=False, null=True)
    message = models.TextField(max_length=500, blank=False, null=True)
    has_account = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return f"Message from {self.firstname} {self.lastname} - {self.has_account}"


class Rating(models.Model):
    RATING_CHOICES = [
        (0, "no ratings"),
        (1, "like"),
        (2, "dislike"),
        (3, "heart"),
        (4, "flame"),
        (5, "trash"),
    ]
    rate = models.IntegerField(choices=RATING_CHOICES, default=0)
    user = models.ForeignKey(
        User, related_name="user_ratings", default=1, on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user.username}-{self.rate}"
