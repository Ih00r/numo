from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('advertisements/', views.advertisement_list, name='advertisement_list'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_advertisements/', views.my_advertisements_view, name='my_advertisements'),
    path('advertisement/<int:advertisement_id>/', views.advertisement_detail_view, name='advertisement_detail'),
    path('advertisement/<int:advertisement_id>/edit/', views.edit_advertisement, name='edit_advertisement'),
    path('advertisement/<int:advertisement_id>/delete/', views.delete_advertisement_view, name='delete_advertisement'),
    path('profile/', views.view_profile, name='view_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('add_job_advertisement/', views.add_job_advertisement, name='add_job_advertisement'),
    path('job_advertisements/', views.job_advertisements_view, name='job_advertisements'),
    path('job_advertisements/<int:advertisement_id>/', views.job_advertisement_detail_view, name='job_advertisement_detail'),  # Новий маршрут для перегляду деталей оголошення про пошук робітників

    path('my_job_advertisements/', views.my_job_advertisements, name='my_job_advertisements'),
    path('edit/<int:id>/', views.edit_job_advertisement, name='edit_job_advertisement'),
    path('delete/<int:ad_id>/', views.delete_job_advertisement, name='delete_job_advertisement')
]