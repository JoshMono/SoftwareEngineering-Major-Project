from django.forms import ModelForm, TextInput, ModelChoiceField, Form
from .models import Company, Contact

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        
        
