
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.firm_dashboard, name='dashboard'),
    path('dashboard/', views.firm_dashboard, name='dashboard'),
    path('company/<company_id>', views.company_detail, name='company_detail'),
    path('create_firm/', views.create_firm, name='create_firm'),
    path('leads/', views.leads, name='leads'),
    path('lead_create/', views.lead_create, name='lead_create'),
    path('lead_edit/<lead_id>', views.lead_edit, name='lead_edit'),
    path('lead_delete/<lead_id>', views.lead_delete, name='lead_delete'),
    path('lead_detail/<lead_id>', views.lead_detail, name='lead_detail'),
    path('quotes/', views.quotes, name='quotes'),
    path('quote_detail/<quote_id>', views.quote_detail, name='quote_detail'),
    path('invoices/', views.invoices, name='invoices'),
    path('companies/', views.companies, name='companies'),
    path('contacts/', views.contacts, name='contacts'),
]