from rest_framework import serializers
from asignacion_servicios.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'country', 'city', 'street', 'latitude', 'longitude']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_country(self, value):
        if not value.strip():
            raise serializers.ValidationError("El país no puede estar vacío.")
        return value

    def validate_city(self, value):
        if not value.strip():
            raise serializers.ValidationError("La ciudad no puede estar vacía.")
        return value

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("La latitud debe estar entre -90 y 90 grados.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("La longitud debe estar entre -180 y 180 grados.")
        return value

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        if (latitude is None and longitude is not None) or (latitude is not None and longitude is None):
            raise serializers.ValidationError("Ambas coordenadas (latitud y longitud) deben estar presentes o ninguna.")

        instance = getattr(self, 'instance', None)
        queryset = Address.objects.filter(
            city=attrs.get('city', instance.city if instance else None),
            country=attrs.get('country', instance.country if instance else None),
            street=attrs.get('street', instance.street if instance else None),
            latitude=latitude if latitude is not None else (instance.latitude if instance else None),
            longitude=longitude if longitude is not None else (instance.longitude if instance else None)
        )
        
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Esta dirección ya existe.")

        return attrs
