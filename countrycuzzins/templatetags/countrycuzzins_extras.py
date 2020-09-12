import os
import re
import base64
import json
from django import template
from ..models import Image, SocialMedia, Video

register = template.Library()


@register.filter("image_get")
def image_get(model, args):
    """ Check Image modes attribute and return the corresponding object
  Args:
      model (Models.Model): HTML Model String
      key (string): "Image model attribute"
      value (string|int|bool): value of attribute
  Returns:
       string: return model atrribute (if exists)
  """
    try:
        key, value, *index = args.split(",")
        img = Image.objects.filter(**{key: value})
        if img:
            # if there are more than one showcase image, then we choose an index
            # default index 0 (objects.first)
            index = int(index[0]) if index else 0
            return img.all()[index].image.url
    except:
        pass


@register.filter("img64")
def img64(obj):
    """Convert  images to base64 data """
    try:
        with open("static/" + obj, "rb") as f:
            data = f.read()
            img = base64.encodebytes(data)
            return f"data:image/png;base64,{str(img.decode('utf8'))}"
    except Exception as error:
        print("\nERROR", error)
        return obj


@register.filter("space_escape")
def space_escape(value):
    return value.replace(" ", "_")


@register.filter("re_sub")
def re_sub(value, ret):
    value = str(value)
    try:
        pat, sub = ret.split(",")
        return re.sub(pat, sub, value)
    except ValueError:  # if ret is string and not a tuple
        pat = ret
        sub = " "
        return re.sub(pat, sub, value)
    except:
        return value


@register.filter("social_get")
def social_get(name, data):
    """Get Social media link by name
    Args:
        name (str): name of social media site
        data (str): model attribute to return

    Returns:
        dict: social media model dictionary
    """
    try:
        social = SocialMedia.objects.filter(
            name__iregex=rf"[.*[\w\s]*.*{name}[\w.\s]*")
        print("\nNAME,DATA", name, data)
        print("\nsocial", social)
        if social:
            return getattr(social.first(), data)
        return {"name": "N/A", "link": "#"}[data]
    except:
        return "N/A"


@register.filter("model_get")
def model_get(model, kwargs):
    """ Retrieve an object from model

    Args:
        model (models.Model): models.Model instance
        kwargs (string dict): dictionary key and value to return
    """
    try:
        # convert the kwargs string into dict
        print('Video Kwargs before:', kwargs)
        kwargs = json.loads(re.sub(r'\'', '\"', kwargs))
        print('Video Kwargs:', kwargs)
        video = Video.objects.filter(**kwargs)

        if video:
            return video.first()
        return " "
    except Exception as e:
        print('Video extra Error', e)
        return "N/A"
