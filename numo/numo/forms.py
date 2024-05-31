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
        labels = {'username': 'Нік користувача'}


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
        labels = {
            'title': 'Заголовок',
            'description': 'Опис',
            'min_age': 'Мінімальний вік',
            'max_age': 'Максимальний вік',
            'city': 'Місто',
            'phone_number': 'Номер телефону',
            'payment': 'Оплата',
            'danger': 'Рівень небезпеки',
        }


class CharityForm(forms.ModelForm):
    class Meta:
        model = Charity
        fields = ['title', 'description', 'min_age', 'max_age', 'city', 'phone_number', 'danger_class']


class AdvertisementFilterForm(forms.Form):
    age = forms.IntegerField(required=False, label='Вік')
    min_age = forms.IntegerField(required=False, label='Мінімальний вік')
    max_age = forms.IntegerField(required=False, label='Максимальний вік')
    city = forms.ChoiceField(required=False, label='Місто')
    danger = forms.ChoiceField(required=False, choices=[('', 'Всі'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], label='Клас небезпеки')
    min_payment = forms.DecimalField(required=False, label='Мінімальна оплата', min_value=0)
    danger_class = forms.ChoiceField(
        required=False,
        choices=[('', 'Всі')] + [(choice, choice) for choice in ['A', 'B', 'C', 'D']],
        label='Клас небезпеки'
    )

    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities', [])
        super().__init__(*args, **kwargs)
        self.fields['city'].choices = [('', 'Всі')] + [(city, city) for city in sorted(cities)]