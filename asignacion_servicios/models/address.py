from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Address(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True)   

    latitude = models.FloatField(validators=[
        MinValueValidator(-90.0),
        MaxValueValidator(90.0)
    ])
    longitude = models.FloatField(validators=[
        MinValueValidator(-180.0),
        MaxValueValidator(180.0)
    ])

    def __str__(self):
        return f"{self.name} — {self.city}, {self.country}"

    class Meta:
        constraints = [
        models.UniqueConstraint(
                fields=['city', 'country', 'street', 'postal_code', 'latitude', 'longitude'],
                name='unique_address'
            )
        ]

        db_table = 'addresses'
        ordering = ['country', 'city', 'name']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'