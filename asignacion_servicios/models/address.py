from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Address(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True, null=True)

    latitude = models.FloatField(validators=[
        MinValueValidator(-90.0),
        MaxValueValidator(90.0)
    ])
    longitude = models.FloatField(validators=[
        MinValueValidator(-180.0),
        MaxValueValidator(180.0)
    ])

    def __str__(self):
        return f"{self.name} — {self.street or 'Sin calle'}, {self.city}, {self.country}"

    def clean(self):
        if (self.latitude is None and self.longitude is not None) or (self.latitude is not None and self.longitude is None):
            raise ValidationError("Ambas coordenadas (latitud y longitud) deben estar presentes o ninguna.")
        super().clean()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'country', 'street', 'latitude', 'longitude'],
                name='unique_address'
            )
        ]
        db_table = 'addresses'
        ordering = ['country', 'city', 'name']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'