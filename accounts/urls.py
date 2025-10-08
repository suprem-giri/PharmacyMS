from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Prescription URLs
    path('customers/<int:customer_pk>/prescriptions/', views.prescription_list, name='prescription_list'),
    path('customers/<int:customer_pk>/prescriptions/add/', views.prescription_create, name='prescription_create'),
    path('customers/<int:customer_pk>/prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('customers/<int:customer_pk>/prescriptions/<int:pk>/delete/', views.prescription_delete, name='prescription_delete'),

    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # User Approval URLs
    path('user-approvals/', views.user_approval_list, name='user_approval_list'),
    path('user-approvals/<int:pk>/approve/', views.approve_user, name='approve_user'),
]
