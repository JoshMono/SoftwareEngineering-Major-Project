from django.forms import ModelForm, TextInput, ModelChoiceField, Form
from .models import Company, Contact, Firm, Lead

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
