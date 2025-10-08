from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
from .models import Sale, SaleItem, Purchase, PurchaseItem
from .forms import SaleForm, SaleItemFormSet, PurchaseForm, PurchaseItemFormSet
from medicines.models import Medicine
from accounts.models import Customer
from suppliers.models import Supplier

@login_required
def sale_list(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    sales = Sale.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')

    if search_query:
        sales = sales.filter(
            Q(customer__name__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    context = {
        'sales': sales,
        'search_query': search_query,
    }
    return render(request, 'sales/sale_list.html', context)

@login_required
def sale_create(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                sale.staff = request.user
                # Initialize total_amount to zero before saving
                sale.total_amount = Decimal('0.00')
                sale.final_amount = Decimal('0.00')
                sale.save()

                total_amount = Decimal('0.00')
                for item_form in formset:
                    if item_form.cleaned_data:
                        item = item_form.save(commit=False)
                        item.sale = sale
                        item.total_price = item.quantity * item.unit_price
                        item.save()
                        total_amount += item.total_price

                        # Update medicine quantity
                        medicine = item.medicine
                        medicine.quantity -= item.quantity
                        medicine.save()

                # Set total amount and calculate final amount with discount and tax
                sale.total_amount = total_amount
                discount_amount = (total_amount * sale.discount) / 100
                taxable_amount = total_amount - discount_amount
                tax_amount = (taxable_amount * sale.tax) / 100
                sale.final_amount = taxable_amount + tax_amount
                sale.save()

                messages.success(request, f'Sale created successfully! Invoice #{sale.id}')
                return redirect('sales:sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
        formset = SaleItemFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'Create Sale'
    }
    return render(request, 'sales/sale_form.html', context)

@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()

    # Calculate discount and tax amounts for display
    discount_amount = (sale.total_amount * sale.discount) / 100 if sale.discount > 0 else Decimal('0.00')
    taxable_amount = sale.total_amount - discount_amount
    tax_amount = (taxable_amount * sale.tax) / 100 if sale.tax > 0 else Decimal('0.00')

    context = {
        'sale': sale,
        'items': items,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
    }
    return render(request, 'sales/sale_detail.html', context)

@login_required
def purchase_list(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    purchases = Purchase.objects.all().order_by('-purchase_date')
    search_query = request.GET.get('search', '')

    if search_query:
        purchases = purchases.filter(
            Q(supplier__name__icontains=search_query) |
            Q(invoice_number__icontains=search_query)
        )

    context = {
        'purchases': purchases,
        'search_query': search_query,
    }
    return render(request, 'sales/purchase_list.html', context)

@login_required
def purchase_create(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)
                purchase.staff = request.user
                purchase.save()

                total_amount = Decimal('0.00')
                for item_form in formset:
                    if item_form.cleaned_data:
                        item = item_form.save(commit=False)
                        item.purchase = purchase
                        item.save()
                        total_amount += item.quantity * item.unit_price

                        # Update medicine quantity and details
                        medicine = item.medicine
                        medicine.quantity += item.quantity
                        medicine.price = item.unit_price  # Update price
                        medicine.expiry_date = item.expiry_date
                        medicine.batch_no = item.batch_number
                        medicine.save()

                purchase.total_amount = total_amount
                purchase.save()

                messages.success(request, f'Purchase created successfully! Invoice #{purchase.invoice_number}')
                return redirect('sales:purchase_detail', pk=purchase.pk)
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'Create Purchase'
    }
    return render(request, 'sales/purchase_form.html', context)

@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    items = purchase.items.all()
    context = {
        'purchase': purchase,
        'items': items,
    }
    return render(request, 'sales/purchase_detail.html', context)
