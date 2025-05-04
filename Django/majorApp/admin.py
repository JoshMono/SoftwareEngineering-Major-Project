from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from . import models

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('dob', 'phone_number',  'firm')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('dob', 'phone_number', 'firm')}),
    )



admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Firm)
admin.site.register(models.Company)
admin.site.register(models.Contact)
admin.site.register(models.Lead)
admin.site.register(models.Quote)
admin.site.register(models.QuoteItem)
admin.site.register(models.Invoice)
admin.site.register(models.InvoiceItem)