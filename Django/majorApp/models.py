from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
import datetime


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True,)
    mfa_secret_key = models.CharField(null=True, blank=True, max_length=16) 
    firm = models.ForeignKey("majorApp.Firm", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Firm(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField()
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField()
    address = models.TextField(null=True, blank=True)
    firm = models.ForeignKey("majorApp.Firm", on_delete=models.CASCADE)
    contacts = models.ManyToManyField("majorApp.Contact", null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_firm(self):
        return self.firm

class Contact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    firm = models.ForeignKey("majorApp.Firm", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_firm(self):
        return self.firm


class LeadStatusChoices(models.TextChoices):
    NO_CONTACT = "NC", _("Not Contacted")
    INITIAL_CONTACT = "IC", _("Initial Contact Made")
    QUOTE_SENT = "QS", _("Quote Sent")
    CONVERTED = "C", _("Converted")
    DO_NOT_CONTACT = "DNC", _("Do Not Contact")

class Lead(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact, null=True, blank=True)
    status = models.CharField(choices=LeadStatusChoices.choices, max_length=50, null=False)
    notes = models.TextField(blank=True)
    estimated_value = models.DecimalField(decimal_places=2, max_digits=12)
    last_contact_date = models.DateField(default=datetime.date.today(), null=True, blank=True)

    def __str__(self):
        return f"{self.company} - ${self.estimated_value}"
    
    def get_firm(self):
        return self.company.firm


class QuoteStatusChoices(models.TextChoices):
    DRAFT = "D", _("Draft")
    SENT = "S", _("Sent")
    WON = "W", _("Won")
    LOST = "L", _("Lost")

class Quote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, help_text="Optional to Link to a Lead")
    status = models.CharField(choices=QuoteStatusChoices.choices, max_length=50, null=False)
    notes = models.TextField(blank=True)
    contacts = models.ManyToManyField(Contact, null=True, blank=True)

    def __str__(self):
        return f"{self.company} - ${self.get_total_price()}"

    def get_firm(self):
        return self.company.firm
    
    def get_total_price(self):
        quote_items = self.quoteitem_set.all()
        price = 0
        for item in quote_items:
            price += item.price
        return price

class QuoteItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.price}"

    def get_firm(self):
        return self.quote.company.firm
    
   
class InvoiceStatusChoices(models.TextChoices):
    DRAFT = "D", _("Draft")
    SENT = "S", _("Sent")

class Invoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, help_text="Optional to Link to a Lead")
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, null=True, blank=True, help_text="Optional to Link to a Quote")
    status = models.CharField(choices=InvoiceStatusChoices.choices, max_length=50, null=False)
    notes = models.TextField(blank=True)
    contacts = models.ManyToManyField(Contact, null=True, blank=True)

    def __str__(self):
        return f"{self.company} - ${self.get_total_price()}"

    def get_firm(self):
        return self.company.firm
    
    def get_total_price(self):
        invoice_items = self.invoiceitem_set.all()
        price = 0
        for item in invoice_items:
            price += item.price
        return price

class InvoiceItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.price}"

    def get_firm(self):
        return self.invoice.company.firm