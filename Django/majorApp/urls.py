from django.contrib import admin
from django.urls import path
from . import views
from allauth.account.views import LoginView, SignupView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),

    ### Login/Signup
    path("accounts/signup/", views.CustomSignupView.as_view(), name="account_signup"),

    path('create_firm/', views.create_firm, name='create_firm'),

    ### Companies
    path('company/<company_id>', views.company_detail, name='company_detail'),
    path('companies/', views.companies, name='companies'),
    path('company_create/', views.company_create, name='company_create'),
    path('company_edit/<company_id>', views.company_edit, name='company_edit'),
    path('company_delete/<company_id>', views.company_delete, name='company_delete'),


    ### Contact
    path('contacts/', views.contacts, name='contacts'),
    path('contact_detail/<contact_id>', views.contact_detail, name='contact_detail'),
    path('contact_create/', views.contact_create, name='contact_create'),
    path('contact_edit/<contact_id>', views.contact_edit, name='contact_edit'),
    path('contact_delete/<contact_id>', views.contact_delete, name='contact_delete'),
    
    
    ### Leads
    path('leads/', views.leads, name='leads'),
    path('lead_create/', views.lead_create, name='lead_create'),
    path('lead_edit/<lead_id>', views.lead_edit, name='lead_edit'),
    path('lead_delete/<lead_id>', views.lead_delete, name='lead_delete'),
    path('lead_detail/<lead_id>', views.lead_detail, name='lead_detail'),

    ### Quotes
    path('quotes/', views.quotes, name='quotes'),
    path('get_quotes/', views.get_quotes, name='get_quotes'),
    path('quote_create/', views.quote_create, name='quote_create'),
    path('quote_edit/<quote_id>', views.quote_edit, name='quote_edit'),
    path('quote_delete/<quote_id>', views.quote_delete, name='quote_delete'),
    path('quote_detail/<quote_id>', views.quote_detail, name='quote_detail'),

    ### Invoices
    path('invoices/', views.invoices, name='invoices'),
    path('get_invoices/', views.get_invoices, name='get_invoices'),
    path('invoice_create/', views.invoice_create, name='invoice_create'),
    path('invoice_edit/<invoice_id>', views.invoice_edit, name='invoice_edit'),
    path('invoice_delete/<invoice_id>', views.invoice_delete, name='invoice_delete'),
    path('invoice_detail/<invoice_id>', views.invoice_detail, name='invoice_detail'),

    
]