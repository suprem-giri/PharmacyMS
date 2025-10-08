from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'company', 'contact_no', 'email', 'address')
    search_fields = ('name', 'company', 'contact_no', 'email')
    list_filter = ('company',)
    ordering = ('name',)
