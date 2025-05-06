from django.forms import ModelForm, TextInput, ModelChoiceField, Form
from .models import Company, Contact, Firm

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        
        
class CreateFirmForm(ModelForm):
    class Meta:
        model = Firm
        fields = ["name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        