from django.forms import ModelForm, TextInput, ModelChoiceField, Form, CharField, EmailField, DateField, DateInput, HiddenInput, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Company, Contact, Firm, Lead, CustomUser, Quote, Invoice
from allauth.account.forms import SignupForm


class CustomUserSignupForm(SignupForm):
    username = CharField(max_length=150, required=True)
    first_name = CharField(max_length=30, required=True)
    last_name = CharField(max_length=30, required=True)
    email = EmailField(required=True)
    phone_number = CharField(max_length=15, required=True)
    dob = DateField(required=True, widget=DateInput(attrs={'type': 'date'}))


class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class CreateFirmForm(ModelForm):
    class Meta:
        model = Firm
        fields = ["name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class CreateLeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = ["company", "status", "notes", "estimated_value", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        super().__init__(*args, **kwargs)
        
        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
      


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("estimated_value") < 0:
            self.add_error("estimated_value", "Enter positive amount")



class CreateQuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["company", "status", "notes", "lead", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)
        if company:
            self.fields['company'].initial = company
            self.fields['company'].widget = HiddenInput()
            
        self.fields['lead'].queryset = Lead.objects.filter(company__firm_id=firm_id)
        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
      
class CreateInvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ["company", "status", "notes", "quote", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        company_id = kwargs.pop("company_id", None)
        super().__init__(*args, **kwargs)
        if company_id:
            company = Company.objects.get(id=company_id)
            self.fields['company'].initial = company
            self.fields['company'].widget = HiddenInput()
            
        self.fields['quote'].queryset = Quote.objects.filter(company__firm_id=firm_id)
        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
      

class CreateContactForm(ModelForm):

    companies = ModelMultipleChoiceField(queryset=None, required=False, widget=CheckboxSelectMultiple)

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None) 
        company_id = kwargs.pop("company_id", None) 
        super().__init__(*args, **kwargs)
        if company_id:
            del self.fields["companies"]
        else:
            self.fields["companies"].queryset = Company.objects.filter(firm_id=firm_id)
            self.fields["companies"].initial = self.instance.companies.all()
      