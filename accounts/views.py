from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer, Profile, Prescription
from .forms import UserRegistrationForm, CustomerForm, ProfileForm, PrescriptionForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account is inactive. Please wait for admin approval.')
                return render(request, 'accounts/login.html')
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'customer'})
            if not profile.is_approved:
                messages.error(request, 'Your account is pending approval.')
                return render(request, 'accounts/login.html')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if profile.role == 'customer':
                return redirect('medicines:medicine_list')
            else:
                return redirect('reports:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            if role in ['admin', 'pharmacist', 'staff']:
                user.is_active = False
                is_approved = False
            else:
                user.is_active = True
                is_approved = True
            user.save()
            Profile.objects.create(user=user, role=role, is_approved=is_approved)
            if role in ['admin', 'pharmacist', 'staff']:
                messages.success(request, 'Account created successfully! Please wait for admin approval.')
            else:
                messages.success(request, 'Account created successfully!')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'role': 'admin' if request.user.is_superuser else 'customer' if hasattr(request.user, 'customer') else 'staff'})
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'role': 'admin' if request.user.is_superuser else 'staff'})
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def customer_list(request):
    if request.user.profile.role == 'customer':
        from django.shortcuts import redirect
        return redirect('medicines:medicine_list')
    customers = Customer.objects.all()
    return render(request, 'accounts/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('accounts:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'accounts/customer_form.html', {'form': form})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'accounts/customer_detail.html', {'customer': customer})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('accounts:customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'accounts/customer_form.html', {'form': form, 'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('accounts:customer_list')
    return render(request, 'accounts/customer_confirm_delete.html', {'customer': customer})

@login_required
def prescription_list(request, customer_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    prescriptions = customer.prescriptions.all().order_by('-uploaded_at')
    return render(request, 'accounts/prescription_list.html', {
        'customer': customer,
        'prescriptions': prescriptions
    })

@login_required
def prescription_create(request, customer_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.customer = customer
            prescription.save()
            messages.success(request, 'Prescription uploaded successfully!')
            return redirect('accounts:prescription_list', customer_pk=customer_pk)
    else:
        form = PrescriptionForm()
    return render(request, 'accounts/prescription_form.html', {
        'form': form,
        'customer': customer
    })

@login_required
def prescription_detail(request, customer_pk, pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    prescription = get_object_or_404(Prescription, pk=pk, customer=customer)
    return render(request, 'accounts/prescription_detail.html', {
        'customer': customer,
        'prescription': prescription
    })

@login_required
def prescription_delete(request, customer_pk, pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    prescription = get_object_or_404(Prescription, pk=pk, customer=customer)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully!')
        return redirect('accounts:prescription_list', customer_pk=customer_pk)
    return render(request, 'accounts/prescription_confirm_delete.html', {
        'customer': customer,
        'prescription': prescription
    })

@login_required
def user_approval_list(request):
    if request.user.profile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('reports:dashboard')
    pending_users = Profile.objects.filter(is_approved=False)
    return render(request, 'accounts/user_approval_list.html', {'pending_users': pending_users})

@login_required
def approve_user(request, pk):
    if request.user.profile.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('reports:dashboard')
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.is_approved = True
        profile.user.is_active = True
        profile.user.save()
        profile.save()
        messages.success(request, f'User {profile.user.username} has been approved.')
        return redirect('accounts:user_approval_list')
    return render(request, 'accounts/user_approve_confirm.html', {'profile': profile})
