from django import forms
from string import Template
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.safestring import mark_safe
from .models import Profile, ContactUs


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=80)
    email = forms.EmailField(required=True, max_length=80)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
        help_text="""<ul class="help_text">
                            <li class="help-item"> Choose a strong password.</li>
                            <li class="help-item"> Your password must contain an alphabet character.</li>
                            <li class="help-item"> Your password must be 8 or more characters long.</li>
                            </ul>
                            """,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=80)
    email = forms.EmailField(required=True, max_length=80)

    class Meta:
        model = User
        fields = ["username", "email"]


class ThumbnailWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value and getattr(value, "url", None):
            pass
        html = Template(
            """<img class="form-img-thumbnail" src="{{ user.profile.getImage }}static/media/$link" style="width:50px; height:50px;"/>"""
        )
        return html.substitute(link=value)


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        error_messages={"invalid": "Opps, File must be an Image file only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = Profile
        fields = ["image"]


class ContactUsForm(forms.ModelForm):
    firstname = forms.CharField(required=True, max_length=60)
    lastname = forms.CharField(required=True, max_length=60)
    email = forms.CharField(required=True, max_length=100)

    class Meta:
        model = ContactUs
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            try:
                field.widget.attrs.pop("autofocus", None)
            except:
                pass

    def save(self, commit=True):
        contact = super(ContactUsForm, self).save(commit=False)
        contact.firstname = self.cleaned_data["firstname"]
        contact.lastname = self.cleaned_data["lastname"]
        contact.email = self.cleaned_data["email"]
        if commit:
            contact.save()
        return contact
