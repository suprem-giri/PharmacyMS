from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from sales.models import Sale, Purchase
from medicines.models import Medicine
from accounts.models import Customer

@login_required
def dashboard(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    # Get current date and date ranges
    today = timezone.now().date()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)

    # Sales statistics
    total_sales_today = Sale.objects.filter(created_at__date=today).aggregate(
        total=Sum('final_amount'))['total'] or 0
    total_sales_month = Sale.objects.filter(created_at__gte=this_month).aggregate(
        total=Sum('final_amount'))['total'] or 0

    # Purchase statistics
    total_purchases_month = Purchase.objects.filter(purchase_date__gte=this_month).aggregate(
        total=Sum('total_amount'))['total'] or 0

    # Inventory statistics
    total_medicines = Medicine.objects.count()
    low_stock_medicines = Medicine.objects.filter(quantity__lte=10).count()
    expiring_soon = Medicine.objects.filter(expiry_date__lte=today + timedelta(days=30)).count()

    # Recent sales
    recent_sales = Sale.objects.select_related('customer').order_by('-created_at')[:5]

    # Top selling medicines this month
    top_medicines = Medicine.objects.filter(
        saleitem__sale__created_at__gte=this_month
    ).annotate(
        total_sold=Sum('saleitem__quantity')
    ).order_by('-total_sold')[:5]

    context = {
        'total_sales_today': total_sales_today,
        'total_sales_month': total_sales_month,
        'total_purchases_month': total_purchases_month,
        'total_medicines': total_medicines,
        'low_stock_medicines': low_stock_medicines,
        'expiring_soon': expiring_soon,
        'recent_sales': recent_sales,
        'top_medicines': top_medicines,
        'profit': total_sales_month - total_purchases_month,
    }

    return render(request, 'reports/dashboard.html', context)

@login_required
def sales_report(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        start_date = timezone.now().date() - timedelta(days=30)
    else:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()

    if not end_date:
        end_date = timezone.now().date()
    else:
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

    sales = Sale.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).select_related('customer', 'staff')

    total_sales = sales.aggregate(total=Sum('final_amount'))['total'] or 0
    total_transactions = sales.count()

    context = {
        'sales': sales,
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_transactions': total_transactions,
    }

    return render(request, 'reports/sales_report.html', context)

@login_required
def inventory_report(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    medicines = Medicine.objects.all().order_by('name')

    # Group by expiry status
    expired = medicines.filter(expiry_date__lt=timezone.now().date())
    expiring_soon = medicines.filter(
        expiry_date__gte=timezone.now().date(),
        expiry_date__lte=timezone.now().date() + timedelta(days=30)
    )
    good_stock = medicines.filter(expiry_date__gt=timezone.now().date() + timedelta(days=30))

    context = {
        'medicines': medicines,
        'expired': expired,
        'expiring_soon': expiring_soon,
        'good_stock': good_stock,
    }

    return render(request, 'reports/inventory_report.html', context)

@login_required
def expiry_report(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    today = timezone.now().date()
    expiry_warning_date = today + timedelta(days=30)

    medicines = Medicine.objects.filter(
        expiry_date__lte=today + timedelta(days=90)
    ).order_by('expiry_date')

    context = {
        'medicines': medicines,
        'today': today,
        'expiry_warning_date': expiry_warning_date,
    }

    return render(request, 'reports/expiry_report.html', context)

@login_required
def profit_loss_report(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        start_date = timezone.now().date() - timedelta(days=30)
    else:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()

    if not end_date:
        end_date = timezone.now().date()
    else:
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Calculate sales revenue
    sales_revenue = Sale.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    # Calculate purchase costs
    purchase_costs = Purchase.objects.filter(
        purchase_date__gte=start_date,
        purchase_date__lte=end_date
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate profit/loss
    profit_loss = sales_revenue - purchase_costs

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'sales_revenue': sales_revenue,
        'purchase_costs': purchase_costs,
        'profit_loss': profit_loss,
    }

    return render(request, 'reports/profit_loss_report.html', context)

@login_required
def export_report(request, report_type):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    # This would implement CSV/PDF export functionality
    # For now, just redirect back
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'

    # Add CSV content here based on report_type
    response.write("Report export functionality to be implemented")

    return response
