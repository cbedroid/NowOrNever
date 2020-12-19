from django import forms
from django.contrib.auth.models import User
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    firstname = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(attrs={"class": "cf-fname"}),
    )
    lastname = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(attrs={"class": "cf-lname"}),
    )
    email = forms.EmailField(
        required=True,
        max_length=80,
        widget=forms.TextInput(attrs={"class": "cf-email"}),
    )
    message = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"class": "cf-message"}),
    )
    ip_address = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ContactUs
        fields = ["firstname", 'lastname', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remove annoying autofocus
        for field in self.fields:
            try:
                field.widget.attrs.pop("autofocus", None)
            except BaseException:
                pass

    def check_contact_has_account(self, form):
        """ Check if the anonomyous user has account with us"""
        if form.is_valid():
            email = self.cleaned_data["email"]
            account = User.objects.filter(email__iexact=email.strip())
            if account.exists():
                form.cleaned_data['has_account'] = True
                form.save()

    def save(self, commit=True, **kwargs):
        contact = super(ContactUsForm, self).save(commit=False)
        contact.firstname = self.cleaned_data["firstname"]
        contact.lastname = self.cleaned_data["lastname"]
        contact.email = self.cleaned_data["email"]
        contact.ip_address = self.cleaned_data["ip_address"]
        contact.has_account = self.cleaned_data["has_account"]
        if commit:
            contact.save()
        return contact
