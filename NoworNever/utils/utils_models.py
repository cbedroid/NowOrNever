import os
import re
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

#########################################################
#           *************************                   #
#           ****  HELP METHODS   ****                   #
#           *************************                   #
#########################################################
""" These methods will be shared throughtout project's apps"""

class OverwriteStorage(FileSystemStorage):
  def get_available_name(self, name, max_length=None):
    self.delete(name)
    return name


def generateSlug(instance):
  """ Add additional help to Admin model site slugfield fields. 
      Build slugfield help text from site deployed ip and port.

      Hacky way to Build SlugField using ip and/or port of website.
      Using javascript instead of python to get url address


  Args:
      instance (models.Model): instance of models.Model
  """
  slug_url = instance.slug +";"
  html = "".join(('''<span id="myslughelp"></span><script>
        const full = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
        const myhelp = document.getElementById("myslughelp");
        const data = myhelp.parentElement.innerHTML;
        myhelp.innerHTML = full + /article/''' ,slug_url , 
        '''alert('Custom ranned');
      </script>'''
      ))
  instance._meta.get_field('slug').help_text  = html



class Command(BaseCommand):
  """ pre-parser hook to change HTML text before rendering to admin """

  def create_parser(self, *args, **kwargs):
    parser = super(Command, self).create_parser(*args, **kwargs)
    parser.formatter_class = RawTextHelpFormatter
    return parser


def adminSlugHelp(instance, views_url=""):
  """
    Hacky way to Build SlugField using ip and/or port of website.
    using javascript instead of python to get url address
  """
  url_path="countrycuzzins"
  if views_url:
    # strip the default app name :NOTE not necessary
    # but to ensure that the start of the url is not duplicated 
    # we TRY strip it and adding it by default.
    url_path = os.path.join(url_path , views_url.strip(url_path),instance.slug)
  else:
    url_path = os.path.join(url_path ,instance.slug)

  html = "".join(('''<span id="myslughelp"></span><script>
        try{
        const full = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
        const myhelp = document.getElementById("myslughelp");
        const data = myhelp.parentElement.innerHTML;
        console.log("Slug_help_parent",data);
        myhelp.innerText = `${full}/%s`
        console.log('Custom ranned');
        }catch(e){
          alert(e.message);
        }
      </script>'''%(url_path)
      ))
  instance._meta.get_field('slug').help_text  = html


def urlParseSlugField(instance,nametupled,help_text=True):
  """Change slugfield name and url parse to url standard 

  Args:
      instance (models.Model): models.Model class instance
      nametupled (tuple/list/str): string or list of name to populate slugfield's path
      help_text (bool, optional): whether to add slugfield as hidden field in admin interface. Defaults to True.

  Returns:
      [type]: [description]
    """
  #   Create custom url for SlugField from article name on initilization
  if not isinstance(nametupled, (list,tuple)):
    nametupled = nametupled.split(',')
  instance.slug = re.sub(r'[^\w\-]','_', "_".join(list(map(str,nametupled))))
  print('\nSELF.SLUG',instance.slug)
  #instance.save()

  if help_text: # add visual for admin .. shows slug url 
    adminSlugHelp(instance,'album')
  print('\nSlugger was successful')
  return instance

