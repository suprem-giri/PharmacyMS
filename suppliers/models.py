from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
