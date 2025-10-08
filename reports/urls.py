from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sales/', views.sales_report, name='sales_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('expiry/', views.expiry_report, name='expiry_report'),
    path('profit-loss/', views.profit_loss_report, name='profit_loss_report'),
    path('export/<str:report_type>/', views.export_report, name='export_report'),
]
