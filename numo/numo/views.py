from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Advertisement

def home(request):
    return render(request, 'home.html', {})
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Ця електронна пошта вже зареєстрована.')
            else:
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 != password2:
                    messages.error(request, 'Паролі не збігаються.')
                else:
                    user = form.save()
                    login(request, user)
                    return redirect('home')  # Redirect to a different template
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')
        else:
            messages.error(request, 'Неправильне ім\'я користувача або пароль')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def welcome(request):
    user = request.user
    first_name = user.first_name
    last_name = user.last_name

    context = {
        'first_name': first_name,
        'last_name': last_name,
    }

    return render(request, 'welcome.html', context)
@login_required
def add_advertisement(request):
    advertisement_added = False
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            user = request.user
            if Advertisement.objects.filter(user=user).exists():
                advertisement_added = True
            else:
                advertisement = form.save(commit=False)
                advertisement.user = user
                advertisement.save()
                return redirect('advertisement_list')  # Redirect to advertisement list page
    else:
        form = AdvertisementForm()
    return render(request, 'add_advertisement.html', {'form': form, 'advertisement_added': advertisement_added})

def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'advertisement_list.html', {'advertisements': advertisements})