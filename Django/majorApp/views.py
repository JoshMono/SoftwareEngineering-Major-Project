from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Firm, Company, Lead, Quote, Invoice, Contact
from .forms import CreateCompanyForm, CreateFirmForm
from .logic import file_management


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
        
<<<<<<< Updated upstream
        firm_id = request.user.firm.id
        
=======
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream

@login_required
def company_dashboard(request, company_id):

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
    return render(request, "majorApp/company_dashboard.html", context)def test_page(request):
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

>>>>>>> Stashed changes
