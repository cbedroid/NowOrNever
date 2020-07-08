import os 
import base64
from django import template
from ..models import Image

register = template.Library()
@register.filter('image_get')
def image_get(model,args):
  """ Check Image modes attribute and return the corresponding object 
  Args:
      model (Models.Model): HTML Model String
      key (string): "Image model attribute"
      value (string|int|bool): value of attribute 

  Returns:
       string: return model atrribute (if exists)
  """
  try:
    key,value,*index = args.split(',')
    img = Image.objects.filter(**{key:value})
    if img:
      # if there are more than one showcase image, then we choose an index 
      index = int(index[0]) if index else 0 # default index 0 (objects.first)
      return img.all()[index].image.url
  except:
    pass

@register.filter('img64')
def img64(obj): 
    """Convert  images to base64 data """ 
    try:
      with open("static/"+obj,'rb') as f: 
        data = f.read()
        img = base64.encodebytes(data)
        return f"data:image/png;base64,{str(img.decode('utf8'))}"
    except Exception as error:
      print('\nERROR',error)
      return obj



