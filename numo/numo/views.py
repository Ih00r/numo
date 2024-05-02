from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views import View
#from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):
    return render(request, 'home.html', {})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a different template
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})





def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильне ім\'я користувача або пароль')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to a different template
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})
#
#
#
#
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Неправильне ім\'я користувача або пароль')
#             return redirect('login')
#     else:
#         return render(request, 'registration/register.html')
