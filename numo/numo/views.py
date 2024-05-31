from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, AdvertisementForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Advertisement, JobAdvertisement, Charity
from .forms import JobAdvertisementForm, CharityForm, AdvertisementFilterForm


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
                return redirect('advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'add_advertisement.html', {'form': form, 'advertisement_added': advertisement_added})

def advertisement_list(request):
    advertisements = Advertisement.objects.all()

    if request.method == 'GET':
        form = AdvertisementFilterForm(request.GET, cities=Advertisement.objects.values_list('city', flat=True).distinct())
        if form.is_valid():
            min_age = form.cleaned_data.get('min_age')
            max_age = form.cleaned_data.get('max_age')
            city = form.cleaned_data.get('city')

            if min_age is not None:
                advertisements = advertisements.filter(age__gte=min_age)
            if max_age is not None:
                advertisements = advertisements.filter(age__lte=max_age)
            if city:
                advertisements = advertisements.filter(city=city)
    else:
        form = AdvertisementFilterForm(cities=Advertisement.objects.values_list('city', flat=True).distinct())

    return render(request, 'advertisement_list.html', {'form': form, 'advertisements': advertisements})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.exclude(pk=user.pk).filter(username=username).exists():
                messages.error(request, 'Цей нік користувача вже використовується.')
            elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, 'Користувач з такою електронною поштою вже існує.')
            else:
                form.save()
                return redirect('welcome')
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


def my_advertisements_view(request):
    user = request.user
    advertisements = Advertisement.objects.filter(user=user)
    return render(request, 'my_advertisements.html', {'advertisements': advertisements})

def advertisement_detail_view(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, id=advertisement_id)
    return render(request, 'advertisement_detail.html', {'advertisement': advertisement})



def delete_advertisement_view(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, id=advertisement_id)
    if request.method == 'POST':
        advertisement.delete()
        return redirect('my_advertisements')
    return render(request, 'home.html', {'advertisement': advertisement})


def edit_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('advertisement_detail', advertisement_id=advertisement_id)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'edit_advertisement.html', {'advertisement': advertisement})

@login_required
def view_profile(request):
    user = request.user
    advertisements = Advertisement.objects.filter(user=user)
    job_advertisements = JobAdvertisement.objects.filter(user=user)
    return render(request, 'view_profile.html', {
        'user': user,
        'advertisements': advertisements,
        'job_advertisements': job_advertisements
    })


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user_advertisements = Advertisement.objects.filter(user=request.user)
        user_advertisements.delete()
        user_job_advertisements = JobAdvertisement.objects.filter(user=request.user)
        user_job_advertisements.delete()
        request.user.delete()
        return redirect('home')
    return redirect('edit_profile')


@login_required
def add_job_advertisement(request):
    if request.method == 'POST':
        form = JobAdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('job_advertisements')  # Перенаправлення на список оголошень
    else:
        form = JobAdvertisementForm()
    return render(request, 'add_job_advertisement.html', {'form': form})


def job_advertisements_view(request):
    job_advertisements = JobAdvertisement.objects.all()

    if request.method == 'GET':
        form = AdvertisementFilterForm(request.GET,
                                          cities=JobAdvertisement.objects.values_list('city', flat=True).distinct())
        if form.is_valid():
            age = form.cleaned_data.get('age')
            city = form.cleaned_data.get('city')
            danger = form.cleaned_data.get('danger')
            min_payment = form.cleaned_data.get('min_payment')

            if age is not None:
                job_advertisements = job_advertisements.filter(min_age__lte=age, max_age__gte=age)
            if city:
                job_advertisements = job_advertisements.filter(city=city)
            if danger:
                job_advertisements = job_advertisements.filter(danger=danger)
            if min_payment is not None:
                job_advertisements = job_advertisements.filter(payment__gte=min_payment)
    else:
        form = AdvertisementFilterForm(cities=JobAdvertisement.objects.values_list('city', flat=True).distinct())

    return render(request, 'job_advertisements.html', {'form': form, 'job_advertisements': job_advertisements})

def my_job_advertisements(request):
    user = request.user
    job_advertisements = JobAdvertisement.objects.filter(user=user)
    return render(request, 'my_job_advertisements.html', {'job_advertisements': job_advertisements})


def edit_job_advertisement(request, id):
    advertisement = get_object_or_404(JobAdvertisement, id=id)
    if request.method == 'POST':
        form = JobAdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('edit_job_advertisement', id=advertisement.id)
    else:
        form = JobAdvertisementForm(instance=advertisement)
    return render(request, 'edit_job_advertisement.html', {'form': form})


def delete_job_advertisement(request, ad_id):
    advertisement = get_object_or_404(JobAdvertisement, id=ad_id)

    if request.method == 'POST':
        advertisement.delete()
        return redirect('my_job_advertisements')
    return render(request, 'confirm_delete.html', {'advertisement': advertisement})

def job_advertisement_detail_view(request, advertisement_id):
    advertisement = get_object_or_404(JobAdvertisement, id=advertisement_id)
    return render(request, 'job_advertisement_detail.html', {'advertisement': advertisement})

def add_charity_advertisement(request):
    if request.method == 'POST':
        form = CharityForm(request.POST)
        if form.is_valid():
            charity = form.save(commit=False)
            charity.user = request.user
            charity.save()
            return redirect('charity_advertisements')
    else:
        form = CharityForm()
    return render(request, 'add_charity_advertisement.html', {'form': form})

def charity_advertisements(request):
    charities = Charity.objects.all()

    if request.method == 'GET':
        form = AdvertisementFilterForm(request.GET, cities=Charity.objects.values_list('city', flat=True).distinct())
        if form.is_valid():
            age = form.cleaned_data.get('age')
            city = form.cleaned_data.get('city')
            danger_class = form.cleaned_data.get('danger_class')

            if age is not None:
                charities = charities.filter(min_age__lte=age, max_age__gte=age)
            if city:
                charities = charities.filter(city=city)
            if danger_class:
                charities = charities.filter(danger_class=danger_class)
    else:
        form = AdvertisementFilterForm(cities=Charity.objects.values_list('city', flat=True).distinct())

    return render(request, 'charity_advertisements.html', {'form': form, 'charities': charities})

def edit_charity_advertisement(request, charity_id):
    charity = get_object_or_404(Charity, id=charity_id)
    if request.method == 'POST':
        form = CharityForm(request.POST, instance=charity)
        if form.is_valid():
            form.save()
            return redirect('my_charity_advertisements')
    else:
        form = CharityForm(instance=charity)
    return render(request, 'edit_charity.html', {'form': form})

def delete_charity_advertisement(request, charity_id):
    charity = get_object_or_404(Charity, id=charity_id)
    if request.method == 'POST':
        charity.delete()
        return redirect('my_charity_advertisements')
    return render(request, 'delete_charity_advertisement.html', {'charity': charity})

def charity_advertisement_detail(request, charity_id):
    charity = get_object_or_404(Charity, id=charity_id)
    my_charity_advertisements = Charity.objects.filter(user=request.user)
    return render(request, 'charity_advertisement_detail.html', {'charity': charity, 'my_charity_advertisements': my_charity_advertisements})

def my_charity_advertisements(request):
    my_charities = Charity.objects.filter(user=request.user)
    return render(request, 'my_charity_advertisements.html', {'my_charities': my_charities})

