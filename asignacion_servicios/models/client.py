from django.db import models
from django.core.validators import RegexValidator
from .address import Address

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número de teléfono debe tener entre 9 y 15 dígitos.")]
    )
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'