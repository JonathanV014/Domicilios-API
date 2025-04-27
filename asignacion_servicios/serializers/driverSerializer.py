from rest_framework import serializers
from asignacion_servicios.models import Address, Driver
import re

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'address', 'is_available']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("El número de teléfono debe tener entre 9 y 15 dígitos y puede incluir un '+' al inicio.")
        return value

    def validate_address(self, value):
        if not Address.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("La dirección proporcionada no existe.")
        return value

    def validate(self, attrs):
        if not attrs.get('is_available') and not attrs.get('address'):
            raise serializers.ValidationError("Un conductor no disponible debe tener una dirección asociada.")
        return attrs