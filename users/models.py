import os
import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from NoworNever.utils.utils_models import Command, OverwriteStorage, generateSlug
from countrycuzzins.models import Video

MEDIA_ROOT = "static" + settings.MEDIA_ROOT


def user_namespace_path(instance, *args, **kwargs):
    """ Renaming Profile's ImageField path to current username

  Args:
      instance (models.Model): models.Model instance

  Returns:
      str: abspath file path
  """
    # Force all images to be PNG file #
    instance_hash = hash(instance.__class__)

    # optional kwargs if model does NOT have an name attribute
    user = kwargs.get("name", None)

    Image_hash = hash(Profile)
    attr, path, ext = {Image_hash: ["image.url", "images/profile/", ".png"],}.get(
        instance_hash
    )

    attr_name = "".join((instance.user.username, ext))
    print("ATTR_USER", attr_name)

    if attr_name:
        new_image = f"{path}{attr_name}"
    else:
        setattr(instance, attr, attr_name)
        new_image = f"{path}{instance.image.url}{ext}"
    print("\nNEW_IMAGE", new_image)
    return new_image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="images/default_profile.png",
        upload_to=user_namespace_path,
        storage=OverwriteStorage(),
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def getImage(self):
        if os.path.isfile(self.image.path):
            return self.image.url
        default_image = "static/media/images/profidefault_profile.png"
        return default_image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ContactUs(models.Model):
    firstname = models.CharField(max_length=60, blank=False, null=True)
    lastname = models.CharField(max_length=60, blank=False, null=True)
    email = models.CharField(max_length=100, blank=False, null=True)
    message = models.TextField(max_length=500, blank=False, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"Message from {self.firstname} {self.lastname}"

    def get_client_ip(request):
        # For Spamming prevention, we need user ip
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# Delete old Profile Image after being udpated
@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
  Deletes file from filesystem
  when corresponding `MediaFile` object is deleted.
  """
    try:
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
    except:
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
