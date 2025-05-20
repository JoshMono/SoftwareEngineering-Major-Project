from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Firm, Company, Lead, Quote, Invoice, Contact
from .forms import CreateCompanyForm, CreateFirmForm
from .logic import file_management

from .forms import CreateCompanyForm, CreateFirmForm, CreateLeadForm, CustomUserSignupForm
from allauth.account.views import SignupView


class CustomSignupView(SignupView):
    form_class = CustomUserSignupForm
    template_name = "accounts/signup.html"



# Create your views here.
@login_required
def firm_dashboard(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.firm = request.user.firm
            company.save()
            return redirect('/dashboard')
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
            return redirect(f'/dashboard')
        context["form"] = form
        return render(request, "majorApp/create_firm.html", context)
    else:
        context["form"] = CreateFirmForm()
        return render(request, "majorApp/create_firm.html", context)


@login_required
def company_detail(request, company_id):

    company = Company.objects.get(id=company_id)
    firm = company.get_firm()
    
    if firm != request.user.firm:
        return HttpResponseForbidden("Permission Denied")
    context = {}
    context["company"] = company
    
    leads = Lead.objects.filter(Q(company_id=company_id) & (Q(status="IC") | Q(status="QS")))
    quotes = Quote.objects.filter(Q(company_id=company_id) & (Q(status="D") | Q(status="S")))
    invoices = Invoice.objects.filter(Q(company_id=company_id) & (Q(status="D") | Q(status="S")))
    contacts = company.contacts.all()
    context['leads'] = leads
    context['quotes'] = quotes
    context['invoices'] = invoices
    context['contacts'] = contacts

    # context["form"] = CreateFirmForm()

    return render(request, "majorApp/company_detail.html", context)

def test_page(request):
    files = file_management.list_txt_files()  # Always populate the dropdown list

    if request.method == "POST":
        if request.POST.get("action") == "create":
            folder = request.POST.get("folder")
            filename = request.POST.get("filename")
            content = request.POST.get("content")

            try:
                file_management.create_file(folder, filename, content)
                return render(request, "majorApp/test_page.html", {
                    "success": True,
                    "files": file_management.list_txt_files()
                })
            except Exception as e:
                return render(request, "majorApp/test_page.html", {
                    "error": str(e),
                    "files": file_management.list_txt_files()
                })

    elif request.method == "GET":
        if request.GET.get("action") == "search":
            selected_file = request.GET.get("selected_file")
            search_term = request.GET.get("file_search", "").strip()

            if selected_file and search_term:
                count = file_management.search_word_in_file(selected_file, search_term)
                return render(request, "majorApp/test_page.html", {
                    "files": files,
                    "search_result": f"The word '{search_term}' appears {count} time(s) in '{selected_file}'."
                })

    return render(request, "majorApp/test_page.html", {
        "files": files
    })

    



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

@login_required
def lead_create(request):

    firm_id = request.user.firm.id
    if request.method == "POST":
        form = CreateLeadForm(request.POST, firm_id=firm_id)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:     
        form = CreateLeadForm(firm_id=firm_id)
        
    return render(request, "majorApp/lead_create.html", {"form": form, "create_edit": "Create"})


@login_required
def lead_edit(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    firm = lead.get_firm()
    user_firm_id = request.user.firm.id
    
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    if request.method == "POST":
        form = CreateLeadForm(request.POST, instance=lead, firm_id=user_firm_id)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:     
        form = CreateLeadForm(instance=lead, firm_id=user_firm_id)
        
    return render(request, "majorApp/lead_create.html", {"form": form, "create_edit": "Edit"})

@login_required
def lead_delete(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    firm = lead.get_firm()
    user_firm_id = request.user.firm.id
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        lead.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/comfirm_delete.html", {"object": lead})

@login_required
def lead_detail(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    firm = lead.get_firm()
    user_firm_id = request.user.firm.id
    context = {}
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")

    
    context['lead'] = lead
    
    return render(request, "majorApp/lead_detail.html", context)   

