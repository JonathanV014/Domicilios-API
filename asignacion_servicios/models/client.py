from django.db import models
from django.core.validators import RegexValidator
from .address import Address

class Client(models.Model):
    """
    Modelo Client

    Representa un cliente con información personal y de contacto.

    Attributes:
        name (str): Nombre del cliente.
        phone (str): Número de teléfono único, validado por formato internacional.
        email (str): Correo electrónico único.
        address (Address): Dirección asociada al cliente.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe tener entre 9 y 15 dígitos y puede incluir el prefijo '+'."
            )
        ]
    )
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Retorna una representación legible del cliente.

        Returns:
            str: Nombre y teléfono del cliente.
        """
        return f"{self.name} ({self.phone})"

    class Meta:
        """
        Metadatos del modelo Client.

        - db_table: Nombre de la tabla en la base de datos.
        - ordering: Orden por defecto en consultas.
        - verbose_name: Nombre legible singular.
        - verbose_name_plural: Nombre legible plural.
        """
        db_table = 'clients'
        ordering = ['name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'