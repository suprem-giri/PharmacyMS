from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pharmacist', 'Pharmacist'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='prescriptions')
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    prescription_text = models.TextField(blank=True, help_text="Enter prescription details if no file is uploaded")
    prescribed_by = models.CharField(max_length=100, blank=True)
    prescription_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.customer.name} - {self.prescription_date or self.uploaded_at.date()}"
