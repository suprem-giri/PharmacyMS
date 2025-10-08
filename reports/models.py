from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('purchase', 'Purchase Report'),
        ('inventory', 'Inventory Report'),
        ('expiry', 'Expiry Report'),
        ('profit', 'Profit & Loss Report'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.JSONField()  # Store report data as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.report_type}"
