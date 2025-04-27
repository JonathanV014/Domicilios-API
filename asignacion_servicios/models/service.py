from django.db import models
from django.core.exceptions import ValidationError
from .client import Client
from .driver import Driver
from .address import Address

class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    pickup_address = models.ForeignKey(Address, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    estimated_time = models.FloatField(null=True, blank=True) 
    distance = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Service {self.status}"
    class Meta:
        db_table = 'services'
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
