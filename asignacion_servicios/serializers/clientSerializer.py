from rest_framework import serializers
from asignacion_servicios.models import Client
import re

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("El número de teléfono debe tener entre 9 y 15 dígitos y puede incluir un '+' al inicio.")
        return value

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está registrado.")
        return value

    def validate_address(self, value):
        if value is None:
            raise serializers.ValidationError("La dirección es obligatoria.")
        return value