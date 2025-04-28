from rest_framework import serializers
from asignacion_servicios.models import Client
import re

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Client.

    Valida los campos obligatorios, el formato del teléfono, unicidad del email y que la dirección sea obligatoria.
    """

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value: str) -> str:
        """
        Valida que el nombre no esté vacío y solo contenga letras y espacios.

        Args:
            value (str): Nombre del cliente.

        Raises:
            serializers.ValidationError: Si el nombre es inválido.

        Returns:
            str: Nombre validado.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_phone(self, value: str) -> str:
        """
        Valida el formato del número de teléfono.

        Args:
            value (str): Número de teléfono.

        Raises:
            serializers.ValidationError: Si el teléfono es inválido.

        Returns:
            str: Teléfono validado.
        """
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("El número de teléfono debe tener entre 9 y 15 dígitos y puede incluir un '+' al inicio.")
        return value

    def validate_email(self, value: str) -> str:
        """
        Valida que el correo electrónico no esté duplicado.

        Args:
            value (str): Correo electrónico.

        Raises:
            serializers.ValidationError: Si el correo ya está registrado.

        Returns:
            str: Correo validado.
        """
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está registrado.")
        return value

    def validate_address(self, value) -> int:
        """
        Valida que la dirección no sea nula.

        Args:
            value: ID de la dirección.

        Raises:
            serializers.ValidationError: Si la dirección es nula.

        Returns:
            int: ID de la dirección validada.
        """
        if value is None:
            raise serializers.ValidationError("La dirección es obligatoria.")
        return value