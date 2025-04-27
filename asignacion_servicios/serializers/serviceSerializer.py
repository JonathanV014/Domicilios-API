from rest_framework import serializers
from asignacion_servicios.models import Service, Driver, Address

class ServiceSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        allow_null=True,
        required=False
    )
    pickup_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = Service
        fields = ['id', 'pickup_address', 'client', 'driver', 'status', 'estimated_time', 'distance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_estimated_time(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("El tiempo estimado debe ser mayor que 0.")
        return value

    def validate_distance(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("La distancia debe ser mayor que 0.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Service.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"El estado '{value}' no es válido. Los estados permitidos son: {', '.join(valid_statuses)}.")
        return value

    def validate(self, attrs):
        status = attrs.get('status')
        driver = attrs.get('driver')

        if status == 'completed' and driver is None:
            raise serializers.ValidationError("Un servicio completado debe tener un conductor asignado.")

        if status == 'pending' and driver is not None:
            raise serializers.ValidationError("Un servicio pendiente no debe tener un conductor asignado.")

        return attrs