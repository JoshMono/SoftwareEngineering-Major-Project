
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_firm/', views.create_firm, name='create_firm'),
]