from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Sale, SaleItem, Purchase, PurchaseItem

class SaleItemInline(TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('total_price',)

class PurchaseItemInline(TabularInline):
    model = PurchaseItem
    extra = 0

@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'staff', 'total_amount', 'discount', 'tax', 'final_amount', 'payment_method', 'created_at')
    search_fields = ('customer__name', 'staff__username', 'id')
    list_filter = ('payment_method', 'created_at', 'staff')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'medicine', 'quantity', 'unit_price', 'total_price')
    search_fields = ('sale__id', 'medicine__name')
    list_filter = ('sale__created_at',)
    ordering = ('-sale__created_at',)
    readonly_fields = ('total_price',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'supplier', 'staff', 'total_amount', 'purchase_date', 'created_at')
    search_fields = ('supplier__name', 'staff__username', 'invoice_number')
    list_filter = ('purchase_date', 'staff', 'supplier')
    ordering = ('-purchase_date',)
    readonly_fields = ('created_at',)
    inlines = [PurchaseItemInline]

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'medicine', 'quantity', 'unit_price', 'expiry_date', 'batch_number')
    search_fields = ('purchase__invoice_number', 'medicine__name', 'batch_number')
    list_filter = ('expiry_date', 'purchase__purchase_date')
    ordering = ('-purchase__purchase_date',)
