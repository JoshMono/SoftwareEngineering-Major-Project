from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Firm, Company, Lead, Quote, Invoice, Contact, QuoteItem, InvoiceItem
from .forms import CreateCompanyForm, CreateFirmForm, ModelChoiceField, CreateQuoteForm, CreateInvoiceForm, CreateContactForm
from .logic import file_management
from weasyprint import HTML, CSS

from .forms import CreateCompanyForm, CreateFirmForm, CreateLeadForm, CustomUserSignupForm, CreateQuoteItemFormSet, CreateQuoteItemForm, CreateInvoiceItemFormSet
from allauth.account.views import SignupView, LoginView
from allauth.account.forms import LoginForm



def landing_page(request):
    return render(request, "accounts/landing_page.html")


class CustomSignupView(SignupView):
    form_class = CustomUserSignupForm
    template_name = "accounts/signup.html"

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

@login_required
def dashboard(request):
   
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

    return render(request, "majorApp/firm/dashboard.html", context)
    

    
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
        return render(request, "majorApp/firm/create_firm.html", context)
    else:
        context["form"] = CreateFirmForm()
        return render(request, "majorApp/firm/create_firm.html", context)
    

@login_required
def edit_firm(request):

    context = {}
    firm = request.user.firm
    if request.method == "POST":
        form = CreateFirmForm(request.POST, instance=firm)
        if form.is_valid():
            firm_instance = form.save()
            request.user.firm = firm_instance
            request.user.save()
            return redirect(f'/dashboard')
        context["form"] = form
        return render(request, "majorApp/firm/create_firm.html", context)
    else:
        context["form"] = CreateFirmForm(instance=firm)
        return render(request, "majorApp/firm/create_firm.html", context)







###
### Company Views
###

@login_required
def companies(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    
    firm_id = request.user.firm.id
    context = {}

    companies = Company.objects.filter(firm__id=firm_id)
    
    context['companies'] = companies
    
    return render(request, "majorApp/company/companies.html", context)

@login_required
def company_detail(request, company_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    company = Company.objects.get(id=company_id)
    firm = company.get_firm()
    
    if firm != request.user.firm:
        return HttpResponseForbidden("Permission Denied")
    context = {}
    context["company"] = company
    
    leads = Lead.objects.filter(company_id=company_id)
    quotes = Quote.objects.filter(company_id=company_id)
    invoices = Invoice.objects.filter(company_id=company_id)
    contacts = company.contacts.all()
    context['leads'] = leads
    context['quotes'] = quotes
    context['invoices'] = invoices
    context['contacts'] = contacts

    return render(request, "majorApp/company/company_detail.html", context)

@login_required
def company_create(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    if request.method == "POST":
        form = CreateCompanyForm(request.POST, firm_id=request.user.firm.id)
        if form.is_valid():
            
            firm = request.user.firm
            form.instance.firm = firm 
            form.save()
            
            return redirect(f'/company/{form.instance.id}')  
            
    else:     
        
        form = CreateCompanyForm(firm_id=request.user.firm.id)

    return render(request, "majorApp/company/company_create.html", {"form": form, "create_edit": "Create"})


@login_required
def company_edit(request, company_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    
    company = Company.objects.get(id=company_id)
    if request.user.firm != company.firm:
        return HttpResponseForbidden("Permission Denied")
    if request.method == "POST":
        form = CreateCompanyForm(request.POST, instance=company, firm_id=request.user.firm.id)
        if form.is_valid():
            
            firm = request.user.firm
            form.instance.firm = firm 
            form.save()
            return redirect(f'/company/{form.instance.id}')  
    else:     
        form = CreateCompanyForm(firm_id=request.user.firm.id, instance=company)

    return render(request, "majorApp/company/company_create.html", {"form": form, "create_edit": "Edit"})

@login_required
def company_delete(request, company_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    company = Company.objects.get(id=company_id)
    user_firm = company.firm
    if company.firm != request.user.firm:
        return HttpResponseForbidden("Permission Denied")
    
    firm = company.get_firm()
    user_firm_id = request.user.firm.id
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        company.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/general/comfirm_delete.html", {"object": company})







###
### Contact Views
###

@login_required
def contacts(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    firm_id = request.user.firm.id
    context = {}

    contacts = Contact.objects.filter(firm__id=firm_id)
    
    context['contacts'] = contacts
    
    return render(request, "majorApp/contact/contacts.html", context)


def contact_detail(request, contact_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    contact = Contact.objects.get(id=contact_id)
    user_firm = contact.firm

    if request.user.firm != user_firm:
        return HttpResponseForbidden("Permission Denied")
    
    context = {}
    context['contact'] = contact
    
    return render(request, "majorApp/contact/contact_detail.html", context)   

@login_required
def contact_create(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    company_id = request.GET.get("company_id")
    if request.method == "POST":
        form = CreateContactForm(request.POST, firm_id=request.user.firm.id)
        if form.is_valid():
            
            firm = request.user.firm
            form.instance.firm = firm 
            instance = form.save()

            if company_id:
                instance.companies.set([Company.objects.get(id=company_id)])  
                return redirect("company_detail", company_id=company_id)
            else:
                instance.companies.set(form.cleaned_data.get("companies"))

            return redirect("contacts")

    else:     
        form = CreateContactForm(firm_id=request.user.firm.id, company_id=company_id)
    return render(request, "majorApp/contact/contact_create.html", {"form": form, "create_edit": "Create"})


@login_required
def contact_edit(request, contact_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    contact = Contact.objects.get(id=contact_id)
    
    firm = contact.get_firm()
    user_firm = request.user.firm
    
    if firm.id != user_firm.id:
        return HttpResponseForbidden("Permission Denied")
    if request.method == "POST":
        form = CreateContactForm(request.POST, instance=contact, firm_id=user_firm.id)
        if form.is_valid():
            form.firm = user_firm 
            instance = form.save()
            instance.companies.set(form.cleaned_data.get("companies"))
            return redirect('/dashboard')
    else:     
        form = CreateContactForm(instance=contact, firm_id=user_firm.id)
        
    return render(request, "majorApp/contact/contact_create.html", {"form": form, "create_edit": "Edit"})

@login_required
def contact_delete(request, contact_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    contact = Contact.objects.get(id=contact_id)
    firm = contact.get_firm()
    user_firm_id = request.user.firm.id
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        contact.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/general/comfirm_delete.html", {"object": contact})





###
### Lead Views
###



@login_required
def leads(request):
    if request.user.firm == None:
        return redirect("/create_firm")

    firm_id = request.user.firm.id
    context = {}

    leads = Lead.objects.filter(company__firm__id=firm_id)
    
    context['leads'] = leads
    
    return render(request, "majorApp/lead/leads.html", context)

@login_required
def lead_detail(request, lead_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    lead = Lead.objects.get(id=lead_id)
    firm = lead.get_firm()
    user_firm_id = request.user.firm.id
    context = {}
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")

    
    context['lead'] = lead
    
    return render(request, "majorApp/lead/lead_detail.html", context)   

@login_required
def lead_create(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    firm_id = request.user.firm.id
    if request.method == "POST":
        form = CreateLeadForm(request.POST, firm_id=firm_id)
        if form.is_valid():
            form.save()
            if request.GET.get("company_id"):
                return redirect(f'/company/{request.GET.get("company_id")}')    
            return redirect('/dashboard')
    else:     
        company_id = request.GET.get("company_id")
        form = CreateLeadForm(firm_id=firm_id, company_id=company_id)
        
    return render(request, "majorApp/lead/lead_create.html", {"form": form, "create_edit": "Create"})


@login_required
def lead_edit(request, lead_id):
    if request.user.firm == None:
        return redirect("/create_firm")
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
        form = CreateLeadForm(instance=lead, firm_id=user_firm_id, edit=True)
        
    return render(request, "majorApp/lead/lead_create.html", {"form": form, "create_edit": "Edit"})

@login_required
def lead_delete(request, lead_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    lead = Lead.objects.get(id=lead_id)
    firm = lead.get_firm()
    user_firm_id = request.user.firm.id
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        lead.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/general/comfirm_delete.html", {"object": lead})








###
### Quote Views
###
@login_required
def get_quotes(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    company_id = request.GET.get('company_id')

    if request.user.firm != Company.objects.get(id=company_id).firm:
        return HttpResponseForbidden("Permission Denied")
    
    leads = Lead.objects.filter(company_id=company_id)
    data = [{'id': lead.id, 'name': lead.__str__()} for lead in leads]
    return JsonResponse({"leads": data}, safe=False)

@login_required
def quote_pdf(request, quote_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    
    quote = Quote.objects.get(id=quote_id)
    firm = request.user.firm

    if quote.get_firm() != firm:
        return HttpResponseForbidden("Permission Denied")
    
    html_string  = render_to_string('majorApp/quote/pdf_template.html', {
        'quote': quote,
        'firm': firm,
    })

   

    html = HTML(string=html_string)
    result = html.write_pdf()
    

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=quote_{quote.id}.pdf'
    return response


@login_required
def quotes(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    firm_id = request.user.firm.id
    context = {}

    quotes = Quote.objects.filter(company__firm__id=firm_id)
    
    context['quotes'] = quotes
    
    return render(request, "majorApp/quote/quotes.html", context)

def quote_detail(request, quote_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    quote = Quote.objects.get(id=quote_id)
    firm = quote.get_firm()
    user_firm_id = request.user.firm.id
    context = {}
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")

    if quote.lead:
        context['lead_id'] = quote.lead.id
    context['quote'] = quote
    
    return render(request, "majorApp/quote/quote_detail.html", context)   

@login_required
def quote_create(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    context = {}
    firm_id = request.user.firm.id
    if request.method == "POST":
        form_set = CreateQuoteItemFormSet(request.POST, queryset=QuoteItem.objects.none())
        company_id = request.POST.get("company")
        company = Company.objects.get(id=company_id)
        form = CreateQuoteForm(request.POST, firm_id=firm_id, company=company)
        
        if form.is_valid() and form_set.is_valid():
            quote_instance = form.save(commit=False)
            quote_items = form_set.save(commit=False)
            request.user.firm.quote_index += 1
            request.user.firm.save()
            quote_instance.quote_index = request.user.firm.quote_index
            quote_instance.save()
            for quote_item in quote_items:
                quote_item.quote = quote_instance
                quote_item.save()
            
            if request.GET.get("company_id"):
                return redirect(f'/company/{request.GET.get("company_id")}')  
            return redirect('/dashboard')
    else:     
        company_id = request.GET.get("company_id")
        if company_id:
            company = Company.objects.get(id=company_id)
            context["company"] = company
            form = CreateQuoteForm(firm_id=firm_id, company=company)
        else:

            form = CreateQuoteForm(firm_id=firm_id)
        form_set = CreateQuoteItemFormSet(queryset=QuoteItem.objects.none())
        
    context["form_set"] = form_set
    context["form"] = form
    context["create_edit"] = "Create"

    return render(request, "majorApp/quote/quote_create.html", context=context)


@login_required
def quote_edit(request, quote_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    quote = Quote.objects.get(id=quote_id)
    firm = quote.get_firm()
    user_firm_id = request.user.firm.id

    context = {}
    context["company"] = quote.company
    
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        form_set = CreateQuoteItemFormSet(request.POST, queryset=QuoteItem.objects.filter(quote=quote))
        company_id = request.POST.get("company")
        company = Company.objects.get(id=company_id)
        form = CreateQuoteForm(request.POST, instance=quote, firm_id=firm.id, company=company)
        
        if form.is_valid() and form_set.is_valid():
            quote_instance = form.save()
            quote_items = form_set.save(commit=False)
            for quote_item in quote_items:
                quote_item.quote = quote_instance
            form_set.save()

            return redirect('/dashboard') 
    else:     
        form = CreateQuoteForm(instance=quote, firm_id=user_firm_id, company=quote.company, edit=True)
        form_set = CreateQuoteItemFormSet(queryset=QuoteItem.objects.filter(quote=quote).order_by("created_at"))
    

    context["form_set"] = form_set
    context["form"] = form
    context["create_edit"] = "Edit"
        
    
    return render(request, "majorApp/quote/quote_create.html", context=context)

@login_required
def quote_delete(request, quote_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    quote = Quote.objects.get(id=quote_id)
    firm = quote.get_firm()
    user_firm_id = request.user.firm
    if firm != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        quote.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/general/comfirm_delete.html", {"object": quote})







###
### Invoice Views
###

@login_required
def get_invoices(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    company_id = request.GET.get('company_id')
    if request.user.firm != Company.objects.get(id=company_id).firm:
        return HttpResponseForbidden("Permission Denied")
    quotes = Quote.objects.filter(company_id=company_id)
    data = [{'id': quote.id, 'name': quote.__str__()} for quote in quotes]
    return JsonResponse({"quotes": data}, safe=False)

@login_required
def invoice_pdf(request, invoice_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    invoice = Invoice.objects.get(id=invoice_id)
    firm = request.user.firm
    if request.user.firm != invoice.get_firm():
        return HttpResponseForbidden("Permission Denied")
    html_string  = render_to_string('majorApp/invoice/pdf_template.html', {
        'invoice': invoice,
        'firm': firm,
    })

    html = HTML(string=html_string)
    result = html.write_pdf()
    

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.id}.pdf'
    return response


@login_required
def invoices(request):
    if request.user.firm == None:
        return redirect("/create_firm")

    firm_id = request.user.firm.id
    context = {}

    invoices = Invoice.objects.filter(company__firm__id=firm_id)
    
    context['invoices'] = invoices
    
    return render(request, "majorApp/invoice/invoices.html", context)


def invoice_detail(request, invoice_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    invoice = Invoice.objects.get(id=invoice_id)
    firm = invoice.get_firm()
    user_firm_id = request.user.firm.id
    context = {}
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")

    if invoice.quote:
        context['quote_id'] = invoice.quote.id
    context['invoice'] = invoice
    
    return render(request, "majorApp/invoice/invoice_detail.html", context)   

@login_required
def invoice_create(request):
    if request.user.firm == None:
        return redirect("/create_firm")
    context = {}
    firm_id = request.user.firm.id
    if request.method == "POST":
        form_set = CreateInvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.none())
        company_id = request.POST.get("company")
        company = Company.objects.get(id=company_id)
        form = CreateInvoiceForm(request.POST, firm_id=firm_id, company=company)
        
        if form.is_valid() and form_set.is_valid():
            invoice_instance = form.save(commit=False)
            invoice_items = form_set.save(commit=False)
            request.user.firm.invoice_index += 1
            request.user.firm.save()
            invoice_instance.invoice_index = request.user.firm.invoice_index
            invoice_instance.save()
            for invoice_item in invoice_items:
                invoice_item.invoice = invoice_instance
                invoice_item.save()


            if request.GET.get("company_id"):
                return redirect(f'/company/{request.GET.get("company_id")}')  
            return redirect('/dashboard')
    else:     
        company_id = request.GET.get("company_id")
        if company_id:
            company = Company.objects.get(id=company_id)
            context["company"] = company
            form = CreateInvoiceForm(firm_id=firm_id, company=company)
        else:

            form = CreateInvoiceForm(firm_id=firm_id)
        form_set = CreateInvoiceItemFormSet(queryset=InvoiceItem.objects.none())
        
        context["form_set"] = form_set
    context["form"] = form
    context["create_edit"] = "Create"

    return render(request, "majorApp/invoice/invoice_create.html", context=context)


@login_required
def invoice_edit(request, invoice_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    invoice = Invoice.objects.get(id=invoice_id)
    firm = invoice.get_firm()
    user_firm_id = request.user.firm.id

    context = {}
    context["company"] = invoice.company
    
    if firm.id != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        form_set = CreateInvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.filter(invoice=invoice))
        company_id = request.POST.get("company")
        company = Company.objects.get(id=company_id)
        form = CreateInvoiceForm(request.POST, instance=invoice, firm_id=firm.id, company=company)
        if form.is_valid() and form_set.is_valid():
            invoice_instance = form.save()
            invoice_items = form_set.save(commit=False)
            for invoice_item in invoice_items:
                invoice_item.invoice = invoice_instance
            form_set.save()

        return redirect('/dashboard') 
    else:     
        form = CreateInvoiceForm(instance=invoice, firm_id=user_firm_id, company=invoice.company, edit=True)
        form_set = CreateInvoiceItemFormSet(queryset=InvoiceItem.objects.filter(invoice=invoice).order_by("created_at"))
    

    context["form_set"] = form_set
    context["form"] = form
    context["create_edit"] = "Edit"
        
    
    return render(request, "majorApp/invoice/invoice_create.html", context=context)

@login_required
def invoice_delete(request, invoice_id):
    if request.user.firm == None:
        return redirect("/create_firm")
    invoice = Invoice.objects.get(id=invoice_id)
    firm = invoice.get_firm()
    user_firm_id = request.user.firm
    if firm != user_firm_id:
        return HttpResponseForbidden("Permission Denied")
    
    if request.method == "POST":
        invoice.delete()
        return redirect('/dashboard')
         
    return render(request, "majorApp/general/comfirm_delete.html", {"object": invoice})



