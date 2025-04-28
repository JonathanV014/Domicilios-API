from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Address(models.Model):
    """
    Modelo Address

    Representa una dirección geográfica con información de país, ciudad, calle y coordenadas.

    Attributes:
        name (str): Nombre de la dirección o referencia.
        country (str): País de la dirección.
        city (str): Ciudad de la dirección.
        street (str, optional): Calle de la dirección. Puede ser nulo o estar en blanco.
        latitude (float): Latitud geográfica, debe estar entre -90 y 90.
        longitude (float): Longitud geográfica, debe estar entre -180 y 180.

    Métodos:
        __str__(): Retorna una representación legible de la dirección.
        clean(): Valida que ambas coordenadas estén presentes o ninguna.
    """

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    def __str__(self) -> str:
        """
        Retorna una representación legible de la dirección.

        Returns:
            str: Cadena con el nombre, calle, ciudad y país.
        """
        street = self.street if self.street else 'Sin calle'
        return f"{self.name} — {street}, {self.city}, {self.country}"

    def clean(self):
        """
        Valida que ambas coordenadas (latitud y longitud) estén presentes o ninguna.

        Raises:
            ValidationError: Si solo una de las coordenadas está presente.
        """
        lat, lon = self.latitude, self.longitude
        if (lat is None) != (lon is None):
            raise ValidationError("Ambas coordenadas (latitud y longitud) deben estar presentes o ninguna.")
        super().clean()

    class Meta:
        """
        Metadatos del modelo Address.

        - unique_address: Garantiza unicidad por ciudad, país, calle y coordenadas.
        - db_table: Nombre de la tabla en la base de datos.
        - ordering: Orden por defecto en consultas.
        - verbose_name: Nombre legible singular.
        - verbose_name_plural: Nombre legible plural.
        """
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