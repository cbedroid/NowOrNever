from django import forms
from string import Template
from django.utils.safestring import mark_safe
from .models import Video


class ThumbnailWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value and getattr(value, "url", None):
            pass
        html = Template("""$link""")
        return html.substitute(link=value)


class VideoForm(forms.ModelForm):
    thumbnail = forms.CharField(
        max_length=200, widget=ThumbnailWidget, required=False)

    class Meta:
        model = Video
        fields = "__all__"
