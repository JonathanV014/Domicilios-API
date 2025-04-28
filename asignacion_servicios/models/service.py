from django.db import models
from django.core.exceptions import ValidationError
from .client import Client
from .driver import Driver
from .address import Address

class Service(models.Model):
    """
    Modelo Service

    Representa un servicio solicitado por un cliente, con información de dirección de recogida,
    cliente, conductor asignado, estado, tiempo estimado y distancia.

    Attributes:
        pickup_address (Address): Dirección de recogida.
        client (Client): Cliente que solicita el servicio.
        driver (Driver): Conductor asignado al servicio.
        status (str): Estado del servicio ('pending', 'in_progress', 'completed', 'canceled').
        estimated_time (float): Tiempo estimado del servicio.
        distance (float): Distancia estimada del servicio.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
    """

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

    def __str__(self) -> str:
        """
        Retorna una representación legible del servicio.

        Returns:
            str: Descripción del servicio con ID, estado y cliente.
        """
        return f"Service {self.id} - {self.status} ({self.client.name})"

    def clean(self) -> None:
        """
        Valida que un servicio completado tenga un conductor asignado.

        Raises:
            ValidationError: Si el servicio está completado y no tiene conductor.
        """
        if self.status == 'completed' and self.driver is None:
            raise ValidationError("Un servicio completado debe tener un conductor asignado.")

    def mark_as_completed(self) -> None:
        """
        Marca el servicio como completado si está en progreso y tiene conductor.

        Raises:
            ValidationError: Si el servicio no está en progreso o no tiene conductor.
        """
        if self.status != 'in_progress':
            raise ValidationError("Solo se pueden completar servicios que estén en progreso.")
        if self.driver is None:
            raise ValidationError("Un servicio completado debe tener un conductor asignado.")
        self.status = 'completed'
        self.save()

    def save(self, *args, **kwargs) -> None:
        """
        Guarda la instancia del servicio. Si se asigna un conductor y el estado es 'pending',
        cambia el estado automáticamente a 'in_progress'.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos de palabra clave.
        """
        if self.driver is not None and self.status == 'pending':
            self.status = 'in_progress'
        super().save(*args, **kwargs)

    class Meta:
        """
        Metadatos del modelo Service.

        - db_table: Nombre de la tabla en la base de datos.
        - ordering: Orden por defecto en consultas.
        - verbose_name: Nombre legible singular.
        - verbose_name_plural: Nombre legible plural.
        """
        db_table = 'services'
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
