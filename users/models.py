from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image

MEDIA_ROOT = "static" + settings.MEDIA_ROOT
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='images/default_profile.png', upload_to='profile')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)
