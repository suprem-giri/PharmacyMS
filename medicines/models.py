from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    batch_no = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    expiry_date = models.DateField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
