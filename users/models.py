import os
import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from core.utils.utils_models import Command, OverwriteStorage, generateSlug
from countrycuzzins.models import Video


from django.urls import reverse, reverse_lazy
MEDIA_ROOT = "static" + settings.MEDIA_ROOT


def user_namespace_path(instance, *args, **kwargs):
    """Renaming Profile's ImageField path to current username

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
    attr, path, ext = {
        Image_hash: ["image.url", "images/profile/", ".png"],
    }.get(instance_hash)

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
        return "static/media/images/profile/fault_profile.png"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

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
                if "default_profile.png" not in instance.image.path:
                    os.remove(instance.image.path)
    except BaseException:
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
