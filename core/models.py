from django.db import models

# Create your models here.


class ContactUs(models.Model):
    firstname = models.CharField(max_length=60, blank=False, null=True)
    lastname = models.CharField(max_length=60, blank=False, null=True)
    ip_address = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, blank=False, null=True)
    message = models.TextField(max_length=500, blank=False, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"Message from {self.firstname} {self.lastname}"
