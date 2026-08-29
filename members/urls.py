from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_list, name='list'),
    path('add/', views.member_add, name='add'),
    path('<int:member_id>/', views.member_detail, name='detail'),
    path('<int:member_id>/edit/', views.member_edit, name='edit'),
    path('<int:member_id>/delete/', views.member_delete, name='delete'),
]
