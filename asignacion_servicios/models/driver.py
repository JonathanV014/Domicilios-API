from django.db import models
from django.core.validators import RegexValidator
from .address import Address

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message="El número de teléfono debe tener entre 9 y 15 dígitos.")]
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='drivers')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({'Disponible' if self.is_available else 'No disponible'})"

    class Meta:
        db_table = 'drivers'
        ordering = ['name']
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
