from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(ModelAdmin):
    list_display = ('name', 'manufacturer', 'batch_no', 'quantity', 'price', 'expiry_date', 'added_on')
    search_fields = ('name', 'manufacturer', 'batch_no')
    list_filter = ('manufacturer', 'expiry_date', 'added_on')
    ordering = ('-added_on',)
    readonly_fields = ('added_on',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
