from django import forms

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    website = forms.URLField(max_length=200, required=False)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=200, required=True)
    picture = forms.ImageField() 