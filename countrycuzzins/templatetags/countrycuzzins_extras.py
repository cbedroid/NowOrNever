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
    key,value,*_ = args.split(',')
    img = Image.objects.filter(**{key:value})
    if img:
      return img.first().image.url
  except:
    pass



@register.filter(name="has_field")
def has_field(model, field):
    try:
        return getattr(model, field, False)
    except:
        return False


@register.filter(name="get_addon")
def get_addon(model, addon_only=False):
    """ Filter  Extra models  queryset and return only Extra objects with is_addon boolean
        param: model - Extra model object ( see orders.models )
        param: addon_only - boolean
        type:  boolean True -  return Extra.is_addon only
                       False - returns all Extra's objects
    """
    if addon_only == False:
        try:
            addon = list(x for x in model if x.is_addon)
            return addon
        except Exception as e:
            pass
    return model


@register.filter(name="js_addon")
def js_addon(addons):
    if addons and isinstance(addons, list):
        return list(
            {
                "name": x.name,
                "img": x.image.url,
                "price": "0.50" if x.is_addon else "0.00",
            }
            for x in addons
        )


@register.filter(name="has_extra")
def has_extra(model):
    has_toppings = hasattr(model, "num_of_toppings")
    has_addons = getattr(model, "addon", False)

    print(f"\n\nHAS_TOPPINGS: {has_toppings}\nHAS_ADDONS: {has_addons}")
    num_of_toppings = 0
    if has_addons:
        if has_toppings:
            print("\nNUM_TOPPINGS", model.num_of_toppings)
            if model.num_of_toppings < 1:
                return False
        return True
    return False

    pass

