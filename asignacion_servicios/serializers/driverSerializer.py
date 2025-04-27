from rest_framework import serializers
from asignacion_servicios.models import Driver, Address
import re

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'address', 'is_available']
        read_only_fields = ['id']
        
    def validate_name(self, value):
        if value and not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value
    
    def validate_address(self, value):
        if isinstance(value, int):
            try:
                Address.objects.get(pk=value)
            except Address.DoesNotExist:
                raise serializers.ValidationError(f"La dirección con ID {value} no existe.")
        return value
        
    def validate_phone(self, value):
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("El teléfono debe tener entre 9 y 15 dígitos.")
        
        instance = getattr(self, 'instance', None)
        qs = Driver.objects.filter(phone=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un/a Driver con este/a phone.")
        return value