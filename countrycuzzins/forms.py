from django import forms
from .models import Image
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  username = forms.CharField(required=True)
  password1 = forms.CharField(label="Password",widget=forms.PasswordInput(),
    required=True,help_text='''<ul class="help_text">
                            <li class="help-item"> Choose a strong password.</li>
                            <li class="help-item"> Your password must contain an alphabet character.</li>
                            <li class="help-item"> Your password must be 8 or more characters long.</li>
                            </ul>
                            ''')

  class Meta:
    model = User
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
        'password1',
        'password2'
    )

  def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']

    if commit:
        user.save()

    return user


class EditProfileForm(UserChangeForm):
  template_name='/something/else'

  class Meta:
      model = User
      fields = (
          'email',
          'first_name',
          'last_name',
          'password'
      )
