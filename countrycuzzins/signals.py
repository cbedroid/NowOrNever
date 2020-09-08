from django.db.models.signals import pre_save, post_save, post_init
from django.utils.html import format_html
from django.dispatch import receiver
from .models import Video


@receiver(pre_save, sender=Video)
def create_thumbnail(sender, instance, **kwargs):
    # create the video thumbail
    url = f"https://img.youtube.com/vi/{instance.vid_id}/hq{instance.thumbnail_choice}.jpg"
    instance.thumbnail = format_html(
        '<img src="%s" width="150" height="150" />' % (url)
    )


# @receiver(post_save, sender=Video)
# def save_profile(sender, instance, **kwargs):
#     instance.save()
