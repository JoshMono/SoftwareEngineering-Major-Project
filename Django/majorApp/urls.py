from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
<<<<<<< Updated upstream
    path('', views.firm_dashboard, name='firm_dashboard'),
    path('firm_dashboard', views.firm_dashboard, name='firm_dashboard'),
    path('company_dashboard/<company_id>', views.company_dashboard, name='company_dashboard'),
    path('test_page/', views.test_page, name='test_page'),
>>>>>>> Stashed changes
    path('create_firm/', views.create_firm, name='create_firm'),

]