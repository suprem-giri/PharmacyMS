from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Supplier
from .forms import SupplierForm

@login_required
def supplier_list(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    suppliers = Supplier.objects.all().order_by('name')
    search_query = request.GET.get('search', '')

    if search_query:
        suppliers = suppliers.filter(
            Q(name__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'suppliers': suppliers,
        'search_query': search_query,
    }

    return render(request, 'suppliers/supplier_list.html', context)

@login_required
def supplier_create(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Add Supplier'})

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier})

@login_required
def supplier_update(request, pk):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('suppliers:supplier_detail', pk=pk)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'supplier': supplier, 'title': 'Edit Supplier'})

@login_required
def supplier_delete(request, pk):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('suppliers:supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})
