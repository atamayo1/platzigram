from django import forms
from django.contrib.auth.models import User

from users.models import Profile

class SignupForm(forms.Form):
    """ Signup form """
    username = forms.CharField(min_length=4, max_length=50)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())

    def clean_username(self):
        """ Username must be unique """
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use')
        return username

    def clean(self):
        """ Verify password confirmation match. """
        data = super().clean()

        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('Password do not match')
        return data
    
    def save(self):
        """ Create user and profile """
        data = self.cleaned_data
        data.pop('confirm_password')

        user = User.objects.create_user(**data)
        profile = Profile(user=user) 
        profile.save()

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    website = forms.URLField(max_length=200, required=False)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=200)
    picture = forms.ImageField() 