from django.urls import path
from . import views

app_name = 'gyms'

urlpatterns = [
    path('', views.gym_profile, name='profile'),
    path('edit/', views.gym_edit, name='edit'),
]
