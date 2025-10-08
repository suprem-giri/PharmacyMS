from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Medicine
from .forms import MedicineForm

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    search_query = request.GET.get('search', '')

    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(batch_no__icontains=search_query)
        )

    filter_option = request.GET.get('filter', '')
    if filter_option == 'low_stock':
        medicines = medicines.filter(quantity__lte=10)
    elif filter_option == 'expiring_soon':
        medicines = medicines.filter(expiry_date__lte=timezone.now().date() + timedelta(days=30))
    elif filter_option == 'expired':
        medicines = medicines.filter(expiry_date__lt=timezone.now().date())

    context = {
        'medicines': medicines,
        'search_query': search_query,
        'filter_option': filter_option,
        'today': timezone.now().date(),
        'expiry_warning_date': timezone.now().date() + timedelta(days=30),
    }

    return render(request, 'medicines/medicine_list.html', context)

@login_required
def medicine_create(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('medicines:medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicines/medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'medicines/medicine_detail.html', {'medicine': medicine})

@login_required
def medicine_update(request, pk):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('medicines:medicine_detail', pk=pk)
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'medicines/medicine_form.html', {'form': form, 'medicine': medicine, 'title': 'Edit Medicine'})

@login_required
def medicine_delete(request, pk):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, 'Medicine deleted successfully!')
        return redirect('medicines:medicine_list')
    return render(request, 'medicines/medicine_confirm_delete.html', {'medicine': medicine})

@login_required
def medicine_search(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(
        Q(name__icontains=query) |
        Q(manufacturer__icontains=query) |
        Q(batch_no__icontains=query)
    )[:10] 

    context = {
        'medicines': medicines,
        'query': query,
    }
    return render(request, 'medicines/medicine_search.html', context)

@login_required
def low_stock_alert(request):
    medicines = Medicine.objects.filter(quantity__lte=10).order_by('quantity')
    context = {
        'medicines': medicines,
        'alert_type': 'Low Stock',
    }
    return render(request, 'medicines/medicine_alerts.html', context)

@login_required
def expiring_soon(request):
    medicines = Medicine.objects.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gte=timezone.now().date()
    ).order_by('expiry_date')

    context = {
        'medicines': medicines,
        'alert_type': 'Expiring Soon',
    }
    return render(request, 'medicines/medicine_alerts.html', context)
