from django.db import models
from django.core.validators import RegexValidator
from .address import Address

class Driver(models.Model):
    """
    Modelo Driver

    Representa un conductor con información personal, estado de disponibilidad y dirección asociada.

    Attributes:
        name (str): Nombre del conductor.
        phone (str): Número de teléfono único, validado por formato internacional.
        address (Address): Dirección asociada al conductor.
        is_available (bool): Estado de disponibilidad del conductor.
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message="El número de teléfono debe tener entre 9 y 15 dígitos y puede incluir un '+' al inicio."
            )
        ]
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='drivers')
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        """
        Retorna una representación legible del conductor.

        Returns:
            str: Nombre y estado de disponibilidad del conductor.
        """
        return f"{self.name} ({'Disponible' if self.is_available else 'No disponible'})"

    class Meta:
        """
        Metadatos del modelo Driver.

        - db_table: Nombre de la tabla en la base de datos.
        - ordering: Orden por defecto en consultas.
        - verbose_name: Nombre legible singular.
        - verbose_name_plural: Nombre legible plural.
        """
        db_table = 'drivers'
        ordering = ['name']
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
