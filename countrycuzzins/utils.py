# NOTE: CAN BE DELETE as of August 25, 2020 DELETE THIS FILE, FILE HAS BEEN REFACTORED IN NoworNever/utils/ folder

import os
import re

#########################################################
#           *************************                   #
#           ****  HELP METHODS   ****                   #
#           *************************                   #
#########################################################


def admin_js_slugUrl(instance, views_url=""):
    """
    Hacky way to Build SlugField using ip and/or port of website.
    using javascript instead of python to get url address
  """
    url_path = "countrycuzzins"
    if views_url:
        # strip the default app name :NOTE not necessary
        # but to ensure that the start of the url is not duplicated
        # we TRY strip it and adding it by default.
        url_path = os.path.join(url_path, views_url.strip(url_path), instance.slug)
    else:
        url_path = os.path.join(url_path, instance.slug)

    # slug_url = instance.slug +";"
    # url_path = "/".join(url_path,slug_url)
    html = "".join(
        (
            """<span id="myslughelp"></span><script>
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
      </script>"""
            % (url_path)
        )
    )
    print("\nSLUG HACK RANNED")
    instance._meta.get_field("slug").help_text = html


def add_SlugField(instance, namesplits, add_jsurl=True):
    """
    Create custom url for SlugField from article name on initilization
  """
    if not isinstance(namesplits, (list, tuple)):
        namesplits = namesplits.split(",")
    instance.slug = re.sub(r"[^\w\-]", "_", "_".join(list(map(str, namesplits))))
    print("\nSELF.SLUG", instance.slug)
    # instance.save()

    if add_jsurl:  # add visual for admin .. shows slug url
        admin_js_slugUrl(instance, "album")
    print("\nSlugger was successful")
    return instance
