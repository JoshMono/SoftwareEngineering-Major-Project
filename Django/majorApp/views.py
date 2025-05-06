from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Company, Lead, Quote, Invoice
from django.db.models import Q
from .forms import CreateCompanyForm

# Create your views here.
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.firm = request.user.firm
            company.save()
            return redirect('dashboard')
    else:
            
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

        context['form'] = CreateCompanyForm()

        return render(request, "majorApp/dashboard.html", context)
