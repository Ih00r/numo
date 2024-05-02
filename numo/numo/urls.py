from django.urls import path
from . import views
from django.urls import path
from .views import home, register_view, login_view, welcome

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
path('welcome/', views.welcome, name='welcome'),
]
