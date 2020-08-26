from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile



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
        'username',
        'email',
        'password1',
        'password2'
    )

  def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.username = self.cleaned_data['username']
    user.email = self.cleaned_data['email']

    if commit:
      user.save()

    return user


class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image']