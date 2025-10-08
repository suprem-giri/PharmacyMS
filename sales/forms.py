from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem, Purchase, PurchaseItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'discount', 'tax', 'payment_method']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }

SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    fields=['medicine', 'quantity', 'unit_price'],
    extra=1,
    widgets={
        'medicine': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    }
)

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'invoice_number', 'purchase_date']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

PurchaseItemFormSet = inlineformset_factory(
    Purchase, PurchaseItem,
    fields=['medicine', 'quantity', 'unit_price', 'expiry_date', 'batch_number'],
    extra=1,
    widgets={
        'medicine': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
    }
)
