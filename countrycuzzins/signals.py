#NOTE: Dec 2020 REFACTOR THIS WHOLE FILE !!!!!! 

import os
import re
import traceback
from django.utils.html import format_html
from django.dispatch import receiver
from django.conf import settings
from .models import Video, Image
from .music_models import Song,Artist
from django.db.models.signals import (
    pre_init, post_init, pre_save,
    post_save, post_delete,post_migrate
)


@receiver(pre_save, sender=Video)
def auto_create_slugfield(sender, instance, **kwargs):
    """Create custom url for SlugField from model name"""
    if not hasattr(sender, 'slug'):
        return
    # Find model name or title attribute
    try:
        name = instance.name
    except AttributeError:
        try:
            name = instance.title
        except:
            print(
                f'SlugSignalError: Can not create slug for {sender} with id: {instance.id}')
            return

    sender_name = str(sender.__name__).lower()
    if not instance.slug or re.search(rf'{sender_name}-\d*', instance.slug):
        # instance slug was aready created
        return instance.slug
    else:

        pre_save.disconnect(auto_create_slugfield, sender=sender)
        instance.slug = f"{sender_name}-{instance.id}"
        instance.save()
        pre_save.connect(auto_create_slugfield, sender=sender)


@receiver(pre_save, sender=Image)
def nameSpaceImage(sender, instance=None, **kwargs):
    """Change images file path to match Image model name's field.
        Change images file extension to png.

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
    """Rename file path to model name's attribute
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
    print("save_info", save_info)
    save_directory, ext = save_info
    model_name_field = instance.name

    # check if the targeted image has an url field
    # if not then abort all chande and return the current instance untouched
    has_url = getattr(target_image, "url", None)
    if not has_url or not save_info:
        print("\nSignalError: Target image has no url path")
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
            print("\nImage New Path", image_new_path)
            # instance.save()
            return image_new_path
    except Exception as e:
        print("\nE", e)
        traceback.print_exc()


#########################################################
#           *************************                   #
#           ******   VIDEO    *******                   #
#           *************************                   #
#########################################################


def create_thumbnail(title, thumbnail, youtube_video_id):
    # create the video thumbail
    url = f"https://img.youtube.com/vi/{youtube_video_id}/hq{thumbnail}.jpg"
    return format_html(
        '<img class="video-thumbnail" src="%s" width="150" height="150" alt="%s Video Thumbnail"/>'
        % (url, title)
    )


@receiver(pre_save, sender=Video)
def create_youtube_embeded_url(sender, instance, **kwargs):
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
            print(
                f"\nSignalVideoError: Can not detect video url in signals. \n{e}\n")

            return

        if youtube_video_id:
            # Create the embed url
            instance.url = f"https://www.youtube.com/embed/{youtube_video_id}"

    # Disconnect from signal to save changes
    if not youtube_video_id:
        print('Youtube already embed')
        youtube_video_id = re.match(r'.*/(.*)', instance.url)
    pre_save.disconnect(create_youtube_embeded_url, sender=sender)
    # NOTE: this is a potential error if re.search return None
    instance.thumbnail = create_thumbnail(
        instance.title, instance.thumbnail_choice, youtube_video_id.group(1)
    )
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
    """Deletes file from filesystem
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



#NOTE DEC 2020 DONT TOUCH --New Signal Dec 2020 

# @receiver(post_save, sender=Song)
# def songAddMainArtist(sender,instance,created=False,**kwargs):
#     print('\nSender',sender)
#     print('Instance',instance)
#     if not created:
#         if not instance.artist.exists():
#             instance.artist.add(*main_artists)
#             instance.save()
#             print("Song Updated: ",instance.artist.all())
    