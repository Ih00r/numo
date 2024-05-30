from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Advertisement, JobAdvertisement, Charity

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Ім'я", max_length=30, required=False)
    last_name = forms.CharField(label="Фамілія", max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'phone_number', 'city', 'age']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class JobAdvertisementForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement
        fields = ['title', 'description', 'min_age', 'max_age', 'city', 'phone_number', 'payment', 'danger']

class CharityForm(forms.ModelForm):
    class Meta:
        model = Charity
        fields = ['title', 'description', 'min_age', 'max_age', 'city', 'phone_number', 'danger_class']