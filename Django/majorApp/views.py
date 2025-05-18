from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Firm, Company, Lead, Quote, Invoice, Contact
from .forms import CreateCompanyForm, CreateFirmForm


# Create your views here.
@login_required
def firm_dashboard(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.firm = request.user.firm
            company.save()
            return redirect('/firm_dashboard')
    else:
        if request.user.firm == None:
            
            return redirect("/create_firm")
        
        firm_id = request.user.firm.id
        
        context = {}

        firm = Firm.objects.get(id=firm_id)
        companies = Company.objects.filter(firm=firm)
        leads = Lead.objects.filter(Q(company__firm__id=firm_id) & (Q(status="IC") | Q(status="QS")))
        quotes = Quote.objects.filter(Q(company__firm__id=firm_id) & (Q(status="D") | Q(status="S")))
        invoices = Invoice.objects.filter(Q(company__firm__id=firm_id) & (Q(status="D") | Q(status="S")))

        context['firm'] = firm
        context['companies'] = companies
        context['leads'] = leads
        context['quotes'] = quotes
        context['invoices'] = invoices

        context['form'] = CreateCompanyForm()

        return render(request, "majorApp/firm_dashboard.html", context)
    
@login_required
def create_firm(request):
    context = {}
    if request.method == "POST":
        form = CreateFirmForm(request.POST)
        if form.is_valid():
            firm_instance = form.save()
            request.user.firm = firm_instance
            request.user.save()
            return redirect(f'/firm_dashboard')
        context["form"] = form
        return render(request, "majorApp/create_firm.html", context)
    else:
        context["form"] = CreateFirmForm()
        return render(request, "majorApp/create_firm.html", context)


@login_required
def company_detail(request, company_id):

    company = Company.objects.get(id=company_id)
    firm = company.get_firm()
    
    print(request.user.firm==firm)
    if firm != request.user.firm:
        return HttpResponseForbidden("Permission Denied")
    context = {}
    context["company"] = company
    
    leads = Lead.objects.filter(Q(company_id=company_id) & (Q(status="IC") | Q(status="QS")))
    quotes = Quote.objects.filter(Q(company_id=company_id) & (Q(status="D") | Q(status="S")))
    invoices = Invoice.objects.filter(Q(company_id=company_id) & (Q(status="D") | Q(status="S")))
    print(dir(company))
    contacts = company.contacts.all()
    context['leads'] = leads
    context['quotes'] = quotes
    context['invoices'] = invoices
    context['contacts'] = contacts

    # context["form"] = CreateFirmForm()
    return render(request, "majorApp/company_detail.html", context)

@login_required
def leads(request):

    firm_id = request.user.firm.id
    context = {}

    leads = Lead.objects.filter(company__firm__id=firm_id)
    
    context['leads'] = leads
    
    return render(request, "majorApp/leads.html", context)

@login_required
def quotes(request):

    firm_id = request.user.firm.id
    context = {}

    quotes = Quote.objects.filter(company__firm__id=firm_id)
    
    context['quotes'] = quotes
    
    return render(request, "majorApp/quotes.html", context)

@login_required
def invoices(request):

    firm_id = request.user.firm.id
    context = {}

    invoices = Invoice.objects.filter(company__firm__id=firm_id)
    
    context['invoices'] = invoices
    
    return render(request, "majorApp/invoices.html", context)

@login_required
def companies(request):

    firm_id = request.user.firm.id
    context = {}

    companies = Company.objects.filter(firm__id=firm_id)
    
    context['companies'] = companies
    
    return render(request, "majorApp/companies.html", context)


@login_required
def contacts(request):

    firm_id = request.user.firm.id
    context = {}

    contacts = Contact.objects.filter(firm__id=firm_id)
    
    context['contacts'] = contacts
    
    return render(request, "majorApp/contacts.html", context)