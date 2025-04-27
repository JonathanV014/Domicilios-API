from django.db import models
from .address import Address

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='drivers')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.address})"

    class Meta:
        db_table = 'drivers'
        ordering = ['name']
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
