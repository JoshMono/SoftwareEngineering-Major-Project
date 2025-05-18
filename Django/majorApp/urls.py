
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.firm_dashboard, name='firm_dashboard'),
    path('dashboard', views.firm_dashboard, name='dashboard'),
    path('company/<company_id>', views.company_detail, name='company_detail'),
    path('create_firm/', views.create_firm, name='create_firm'),
    path('leads/', views.leads, name='leads'),
    path('quotes/', views.quotes, name='quotes'),
    path('invoices/', views.invoices, name='invoices'),
    path('companies/', views.companies, name='companies'),
    path('contacts/', views.contacts, name='contacts'),
]