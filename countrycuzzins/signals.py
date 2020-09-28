import os
from django.db.models.signals import pre_save, post_delete
from django.utils.html import format_html
from django.dispatch import receiver
from .models import Video, Image, Song


@receiver(pre_save, sender=Video)
def create_thumbnail(sender, instance, **kwargs):
    # create the video thumbail
    url = f"https://img.youtube.com/vi/{instance.vid_id}/hq{instance.thumbnail_choice}.jpg"
    instance.thumbnail = format_html(
        '<img class="video-thumbnail" src="%s" width="150" height="150" alt="%s Video Thumbnail"/>'
        % (url, instance.title)
    )


#########################################################
#           *************************                   #
#           ******   CLEAN UP *******                   #
#           *************************                   #
#########################################################


@receiver(post_delete, sender=Image)
@receiver(post_delete, sender=Song)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ Deletes file from filesystem
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
