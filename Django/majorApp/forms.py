from django.forms import ModelForm, TextInput, ModelChoiceField, Form, CharField, EmailField, modelformset_factory, BaseModelFormSet, DateField, DateInput, HiddenInput, ChoiceField,ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Company, Contact, Firm, Lead, CustomUser, Quote, Invoice, QuoteItem, InvoiceItem
from allauth.account.forms import SignupForm, LoginForm
from django.utils.timezone import now


class CustomUserSignupForm(SignupForm):
    first_name = CharField(max_length=30, required=True)
    last_name = CharField(max_length=30, required=True)
    email = EmailField(required=True)
    phone_number = CharField(max_length=15, required=True)
    dob = DateField(required=True, widget=DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields by setting `self.fields` as an OrderedDict with desired order
        from collections import OrderedDict
        
        desired_order = ['first_name', 'phone_number', 'last_name', 'dob', 'email', 'password1']
        self.fields = OrderedDict(
            (key, self.fields[key]) for key in desired_order if key in self.fields
        )
        
        
class CreateFirmForm(ModelForm):
    class Meta:
        model = Firm
        fields = ["name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput()

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "address", "contacts", "industry"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput()
        self.fields['address'].widget = TextInput()
        self.fields['industry'].widget = TextInput()
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
        

class CreateLeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = ["company", "status", "notes", "estimated_value", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        company_id = kwargs.pop("company_id", None)
        edit = kwargs.pop("edit", False)
        super().__init__(*args, **kwargs)
        if company_id:
            company = Company.objects.get(id=company_id)
            if not edit:
                self.fields['fake_company'] = ChoiceField()
                self.fields['fake_company'].choices = ((1, company),)
                self.fields['fake_company'].label = "Company" 
                self.fields['fake_company'].disabled = True
                self.fields['fake_company'].required = False
                self.fields['company'].initial = company
                self.fields['company'].widget = HiddenInput()
                self.order_fields(["fake_company", "status", "notes", "estimated_value", "last_contact_date", "contacts"])
        
        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
        self.fields['last_contact_date'] = DateField(required=True, initial=now, widget=DateInput(attrs={'type': 'date'}))
      


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("estimated_value") < 0:
            self.add_error("estimated_value", "Enter positive amount")





class CreateQuoteItemForm(ModelForm): 
    class Meta:
        model = QuoteItem
        fields = ['description','price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = True
        self.fields['description'].widget = TextInput()
        self.fields['description'].required = True
        self.fields['price'].required = True

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        
class BaseQuoteItemFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if 'DELETE' in form.fields:
                form.fields['DELETE'].widget.attrs['style'] = ' display: None;'
                form.fields['DELETE'].label = ''

CreateQuoteItemFormSet = modelformset_factory(model=QuoteItem, form=CreateQuoteItemForm, formset=BaseQuoteItemFormSet, extra=1, can_delete=True)


class CreateQuoteForm(ModelForm):
    
    class Meta:
        model = Quote
        fields = ["company", "status", "notes", "lead", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        company = kwargs.pop("company", None)
        edit = kwargs.pop("edit", False)
        super().__init__(*args, **kwargs)
        if company:
            if not edit:
                self.fields['fake_company'] = ChoiceField()
                self.fields['fake_company'].choices = ((1, company),)
                self.fields['fake_company'].label = "Company" 
                self.fields['fake_company'].disabled = True
                self.fields['fake_company'].required = False
                self.fields['company'].initial = company
                self.fields['company'].widget = HiddenInput()
                self.fields['lead'].queryset = Lead.objects.filter(company=company)
                self.order_fields(["fake_company", "status", "notes", "lead", "last_contact_date", "contacts"])
            else:
                self.fields['lead'].queryset = Lead.objects.filter(company=company)
        else:
            self.fields['lead'].queryset = Lead.objects.none()

        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['last_contact_date'] = DateField(required=True, initial=now, widget=DateInput(attrs={'type': 'date'}))
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)




class CreateInvoiceItemForm(ModelForm): 
    class Meta:
        model = InvoiceItem
        fields = ['description','price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = TextInput()
        self.fields['description'].required = True
        self.fields['price'].required = True
        
class BaseInvoiceItemFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if 'DELETE' in form.fields:
                form.fields['DELETE'].widget.attrs['style'] = ' display: None;'
                form.fields['DELETE'].label = ''

CreateInvoiceItemFormSet = modelformset_factory(model=InvoiceItem, form=CreateInvoiceItemForm, formset=BaseInvoiceItemFormSet, extra=1, can_delete=True)
      
class CreateInvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ["company", "status", "notes", "quote", "last_contact_date", "contacts"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None)
        company = kwargs.pop("company", None)
        edit = kwargs.pop("edit", False)
        super().__init__(*args, **kwargs)
        if company:
            if not edit:
                self.fields['fake_company'] = ChoiceField()
                self.fields['fake_company'].choices = ((1, company),)
                self.fields['fake_company'].label = "Company" 
                self.fields['fake_company'].disabled = True
                self.fields['fake_company'].required = False
                self.fields['company'].initial = company
                self.fields['company'].widget = HiddenInput()
                self.fields['quote'].queryset = Quote.objects.filter(company=company)
                self.order_fields(["fake_company", "status", "notes", "quote", "last_contact_date", "contacts"])
            else:
                self.fields['quote'].queryset = Quote.objects.filter(company=company)
        else:
            self.fields['quote'].queryset = Quote.objects.none()

        self.fields['company'].queryset = Company.objects.filter(firm_id=firm_id)
        self.fields['contacts'].queryset = Contact.objects.filter(firm_id=firm_id)
        self.fields['last_contact_date'] = DateField(required=True, initial=now, widget=DateInput(attrs={'type': 'date'}))
      

class CreateContactForm(ModelForm):

    companies = ModelMultipleChoiceField(queryset=None, required=False, widget=CheckboxSelectMultiple)

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        firm_id = kwargs.pop("firm_id", None) 
        company_id = kwargs.pop("company_id", None) 
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget = TextInput()
        self.fields["last_name"].widget = TextInput()
        self.fields["phone_number"].widget = TextInput()
        if company_id:
            del self.fields["companies"]
        else:
            self.fields["companies"].queryset = Company.objects.filter(firm_id=firm_id)
            self.fields["companies"].initial = self.instance.companies.all()
        self.fields['last_contact_date'] = DateField(required=True, widget=DateInput(attrs={'type': 'date'}), initial=now)
      