from django import forms
from .models import Image
from image_cropping import ImageCropWidget

class ImageForm(forms.ModelForm):
    class Meta:
      model = Image
        widgets = {
            'image': ImageCropWidget,
        }