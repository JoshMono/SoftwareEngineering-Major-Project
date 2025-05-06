from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Company, Lead, Quote, Invoice
from django.db.models import Q

# Create your views here.
@login_required
def dashboard(request):
    context = {}

    user = request.user
    firm_id = user.firm.id
    companies = Company.objects.filter(firm=user.firm)
    leads = Lead.objects.filter(Q(company__firm__id=firm_id) & (Q(status="IC") | Q(status="QS")))
    quotes = Quote.objects.filter(Q(company__firm__id=firm_id) & (Q(status="D") | Q(status="S")))
    invoices = Invoice.objects.filter(Q(company__firm__id=firm_id) & (Q(status="D") | Q(status="S")))

    context['companies'] = companies
    context['leads'] = leads
    context['quotes'] = quotes
    context['invoices'] = invoices

    return render(request, "majorApp/dashboard.html", context)
