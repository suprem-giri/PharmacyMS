from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Customer, Profile, Prescription

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('name', 'contact_no', 'email', 'created_at')
    search_fields = ('name', 'contact_no', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'address')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('role',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'prescribed_by', 'prescription_date', 'uploaded_at')
    search_fields = ('customer__name', 'prescribed_by')
    list_filter = ('prescription_date', 'uploaded_at')
    ordering = ('-uploaded_at',)
