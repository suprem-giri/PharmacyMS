from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.medicine_create, name='medicine_create'),
    path('<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('<int:pk>/edit/', views.medicine_update, name='medicine_update'),
    path('<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('search/', views.medicine_search, name='medicine_search'),
    path('low-stock/', views.low_stock_alert, name='low_stock_alert'),
    path('expiring-soon/', views.expiring_soon, name='expiring_soon'),
]
