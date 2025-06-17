from django.contrib import admin
from django.urls import path
from . import views
from allauth.account.views import LoginView, SignupView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),

    ### Account
     path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='account_reset_password'),
     path('accounts/password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
     path('accounts/password/reset/key/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
     path('accounts/password/reset/key/done/', views.landing_page, name='password_reset_complete'),
     
    path("accounts/landing_page/", views.landing_page, name="landing_page"),
    path("accounts/signup/", views.CustomSignupView.as_view(), name="account_signup"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="account_login"),

    path('create_firm/', views.create_firm, name='create_firm'),
    path('edit_firm/', views.edit_firm, name='edit_firm'),

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
    path('quote_pdf/<quote_id>', views.quote_pdf, name='quote_pdf'),
    path('get_quotes/', views.get_quotes, name='get_quotes'),
    path('quote_create/', views.quote_create, name='quote_create'),
    path('quote_edit/<quote_id>', views.quote_edit, name='quote_edit'),
    path('quote_delete/<quote_id>', views.quote_delete, name='quote_delete'),
    path('quote_detail/<quote_id>', views.quote_detail, name='quote_detail'),

    ### Invoices
    path('invoices/', views.invoices, name='invoices'),
    path('invoice_pdf/<invoice_id>', views.invoice_pdf, name='invoice_pdf'),
    path('get_invoices/', views.get_invoices, name='get_invoices'),
    path('invoice_create/', views.invoice_create, name='invoice_create'),
    path('invoice_edit/<invoice_id>', views.invoice_edit, name='invoice_edit'),
    path('invoice_delete/<invoice_id>', views.invoice_delete, name='invoice_delete'),
    path('invoice_detail/<invoice_id>', views.invoice_detail, name='invoice_detail'),

    
]