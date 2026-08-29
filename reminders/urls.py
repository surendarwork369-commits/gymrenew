from django.urls import path

from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.reminder_list, name='list'),
    path('member/<int:member_id>/send/', views.send_member_reminder, name='send_member'),
]
