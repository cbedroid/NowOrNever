# NOTE: Dec 2020 REFACTOR THIS WHOLE FILE !!!!!!

import os
import re
import traceback
from django.utils.html import format_html
from django.dispatch import receiver
from django.conf import settings
from .models import Video, Image
from .music_models import Song, Artist
from django.db.models.signals import (
     pre_save, post_save, post_delete
     )

@receiver(pre_save, sender=Image)
def nameSpaceImage(sender, instance=None, **kwargs):
    """
       Change images file path to match Image model name's field.
       Extension will be changed to png

    Ex: myimage = Image.create(name="hello",image="some_file")
        myimage.image.url  will be changed to --> hello.png
    """
    pre_save.disconnect(nameSpaceImage, sender=sender)
    # Force all images to be PNG file #
    Image_hash = hash(Image)
    attr, path, ext = ["image.url", "images/", ".png"]
    attr_name = "".join((path, instance.name, ext))
    setattr(instance, "image", attr_name.lower())
    instance.save()
    pre_save.connect(nameSpaceImage, sender=sender)


@receiver(post_save, sender=Image)
def pathFromName(sender, **kwargs):
    """
        Rename file path to model name's attribute
        Args:
            sender (class Image ): models.Models Image
            instance (class field):  models.Model class field
            filetype (str):  media field type
            extention (str, optional): extention to assign to path. Defaults to None.

        Returns:
            str: path to file
    """
    # Capture instanceect classname and set the save path and extention
    instance = kwargs.get("instance")
    target_image = instance.image
    Image_hash = hash(sender.image.field)
    save_info = {Image_hash: ["images/", ".png"]}.get(hash(target_image.field))

    # Force Image(sender) to have a name field in model
    # Abort all change if it doesn't
    if not hasattr(sender, "name"):
        return

    # get the name attribute from model
    save_directory, ext = save_info
    model_name_field = instance.name

    # check if the targeted image has an url field
    # if not then abort all chande and return the current instance untouched
    has_url = getattr(target_image, "url", None)
    if not has_url or not save_info:
        return

    image_basename = os.path.basename(instance.image.url)
    try:
        # Get the basename  minus the extention of the url
        image_name, extention = os.path.splitext((image_basename))

        # Check if the image path have previous being change
        # ( basically if this function has already alter this current image. )
        if model_name_field != image_name:  # False then we change this image attributes
            image_new_path = save_directory + str(model_name_field) + ext

            # Change the image current path to the new path
            current_path = os.path.abspath(target_image.path)
            new_path = os.path.join(settings.MEDIA_ROOT, image_new_path)
            try:
                os.rename(current_path, new_path)
            except:
                pass
            return image_new_path
    except Exception as e:
        print("\nE", e)
        traceback.print_exc()


#########################################################
#           *************************                   #
#           ******   VIDEO    *******                   #
#           *************************                   #
#########################################################


def create_thumbnail_cover(title, thumbnail, youtube_video_id):
    # Create the thumbnail covers for video 
    url = f"https://img.youtube.com/vi/{youtube_video_id}/hq{thumbnail}.jpg"
    return format_html(
        '<img class="video-thumbnail" src="%s" width="150" height="150" alt="%s Video Thumbnail"/>'
        % (url, title)
    )


@receiver(pre_save, sender=Video)
def create_youtube_embeded_url(sender, instance, **kwargs):
    """ Convert youtube video to validate embeded format"""
    youtube_url_names = ["youtube", "youtu.be"]
    youtube_video_id = None
    url = instance.url
    if any(x in url for x in youtube_url_names) and "embed" not in url:
        instance.is_youtube = True
        # Convert video's the url into youtube embed format
        try:
            youtube_video_id = re.match(r".*v\=(\w*)", instance.url).group(1)
        except AttributeError:
            youtube_video_id = re.match(r".*/(\w*)", instance.url).group(1)
        except Exception as e:
            return

        if youtube_video_id:
            # Create the embed url
            instance.url = f"https://www.youtube.com/embed/{youtube_video_id}"

    # Disconnect from signal to save changes
    if not youtube_video_id: # video is already converted
        youtube_video_id = re.match(r'.*/(.*)', instance.url)
    pre_save.disconnect(create_youtube_embeded_url, sender=sender)
    # NOTE: this is a potential error if re.search return None
    try:
        instance.thumbnail = create_thumbnail_cover(
            instance.title, instance.thumbnail_choice,
            youtube_video_id.group(1)
        )
    except:
        pass
    instance.save()
    pre_save.connect(create_youtube_embeded_url, sender=sender)


#########################################################
#           *************************                   #
#           ******   CLEAN UP *******                   #
#           *************************                   #
#########################################################


@receiver(post_delete, sender=Image)
@receiver(post_delete, sender=Song)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ Remove deleted file from filesystem """
    try:
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
    except:
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
