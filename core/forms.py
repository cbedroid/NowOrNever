from django import forms
from string import Template
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    firstname = forms.CharField(
        required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'cf-fname'}))
    lastname = forms.CharField(
        required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'cf-lname'}))
    email = forms.EmailField(required=True, max_length=80,
                             widget=forms.TextInput(attrs={'class': 'cf-email'}))
    message = forms.CharField(required=True, max_length=500,
                              widget=forms.Textarea(attrs={'class': 'cf-message'}))
    ip_address = forms.CharField(required=False, widget=forms.HiddenInput())

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

    def save(self, commit=True, **kwargs):
        contact = super(ContactUsForm, self).save(commit=False)
        contact.firstname = self.cleaned_data["firstname"]
        contact.lastname = self.cleaned_data["lastname"]
        contact.email = self.cleaned_data["email"]
        contact.ip_address = self.cleaned_data['ip_address']
        print('\nFrom Forms IP_ADDRESS:', contact.ip_address)
        if commit:
            contact.save()
        return contact
