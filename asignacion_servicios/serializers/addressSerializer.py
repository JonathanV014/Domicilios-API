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

        if Address.objects.filter(
            city=attrs.get('city'),
            country=attrs.get('country'),
            street=attrs.get('street'),
            latitude=latitude,
            longitude=longitude
        ).exists():
            raise serializers.ValidationError("Esta dirección ya existe.")

        return attrs
