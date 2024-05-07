from django.urls import path
from . import views
from django.urls import path
from .views import home, register_view, login_view, welcome, add_advertisement, advertisement_list

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
path('welcome/', views.welcome, name='welcome'),
    path('add/', add_advertisement, name='add_advertisement'),
path('advertisements/', advertisement_list, name='advertisement_list'),
]
