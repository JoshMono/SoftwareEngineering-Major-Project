from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Company, Lead, Quote, Invoice
from django.db.models import Q

# Create your views here.
@login_required
def dashboard(request):
    context = {}

    companies = Company.objects.all()
    leads = Lead.objects.all()
    quotes = Quote.objects.filter(Q(status="S") | Q(status="D"))
    invoices = Invoice.objects.filter(status="D")

    context['companies'] = companies
    context['leads'] = leads
    context['quotes'] = quotes
    context['invoices'] = invoices

    return render(request, "majorApp/dashboard.html", context)
