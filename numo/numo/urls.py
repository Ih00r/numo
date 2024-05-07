from django.urls import path
from . import views
from django.urls import path
from .views import home, register_view, login_view, welcome, add_advertisement, advertisement_list, edit_profile, advertisement_detail_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
path('welcome/', views.welcome, name='welcome'),
    path('add/', add_advertisement, name='add_advertisement'),
path('advertisements/', advertisement_list, name='advertisement_list'),
    path('edit_profile/'  , edit_profile, name='edit_profile'),
path('my_advertisements/', views.my_advertisements_view, name='my_advertisements'),
    path('advertisement/<int:advertisement_id>/', advertisement_detail_view, name='advertisement_detail'),
     path('advertisement/<int:advertisement_id>/edit/', views.edit_advertisement_view, name='edit_advertisement'),
    path('advertisement/<int:advertisement_id>/delete/', views.delete_advertisement_view, name='delete_advertisement'),

]
