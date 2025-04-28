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
        return f"Service {self.id} - {self.status} ({self.client.name})"

    def clean(self):
        if self.status == 'completed' and self.driver is None:
            raise ValidationError("Un servicio completado debe tener un conductor asignado.")

    def mark_as_completed(self):
        if self.status != 'in_progress':
            raise ValidationError("Solo se pueden completar servicios que estén en progreso.")
        if self.driver is None:
            raise ValidationError("Un servicio completado debe tener un conductor asignado.")
        self.status = 'completed'
        self.save()

    def save(self, *args, **kwargs):
        if self.driver is not None and self.status == 'pending':
            self.status = 'in_progress'
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'services'
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        