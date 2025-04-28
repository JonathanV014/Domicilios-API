from rest_framework import serializers
from asignacion_servicios.models import Driver, Address
import re

class DriverSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Driver.

    Valida el nombre, el formato y unicidad del teléfono, y la existencia de la dirección.
    """

    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'address', 'is_available']
        read_only_fields = ['id']

    def validate_name(self, value: str) -> str:
        """
        Valida que el nombre solo contenga letras y espacios.

        Args:
            value (str): Nombre del conductor.

        Raises:
            serializers.ValidationError: Si el nombre es inválido.

        Returns:
            str: Nombre validado.
        """
        if value and not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_address(self, value) -> int:
        """
        Valida que la dirección exista si se pasa como ID.

        Args:
            value (int): ID de la dirección.

        Raises:
            serializers.ValidationError: Si la dirección no existe.

        Returns:
            int: ID de la dirección validada.
        """
        if isinstance(value, int):
            try:
                Address.objects.get(pk=value)
            except Address.DoesNotExist:
                raise serializers.ValidationError(f"La dirección con ID {value} no existe.")
        return value

    def validate_phone(self, value: str) -> str:
        """
        Valida el formato y unicidad del teléfono.

        Args:
            value (str): Teléfono del conductor.

        Raises:
            serializers.ValidationError: Si el teléfono es inválido o no es único.

        Returns:
            str: Teléfono validado.
        """
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("El teléfono debe tener entre 9 y 15 dígitos y puede incluir un '+' al inicio.")

        instance = getattr(self, 'instance', None)
        qs = Driver.objects.filter(phone=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un conductor con este teléfono.")
        return value