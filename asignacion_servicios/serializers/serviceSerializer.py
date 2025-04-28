from rest_framework import serializers
from asignacion_servicios.models import Service, Driver, Address

class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Service.

    Valida el estado, el tiempo estimado, la distancia y las reglas de negocio entre estado y conductor.
    """
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

    def validate_status(self, value: str) -> str:
        """
        Valida el estado del servicio.

        Args:
            value (str): Estado del servicio.

        Raises:
            serializers.ValidationError: Si el estado es inválido o si se intenta cambiar el estado de un servicio completado.

        Returns:
            str: Estado validado.
        """
        if self.instance and self.instance.status == 'completed':
            raise serializers.ValidationError("No se puede cambiar el estado de un servicio ya completado.")
        valid_statuses = [choice[0] for choice in Service.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"El estado '{value}' no es válido. Los estados permitidos son: {', '.join(valid_statuses)}."
            )
        return value

    def validate_estimated_time(self, value: float) -> float:
        """
        Valida que el tiempo estimado sea mayor que 0.

        Args:
            value (float): Tiempo estimado.

        Raises:
            serializers.ValidationError: Si el tiempo no es válido.

        Returns:
            float: Tiempo validado.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError("El tiempo estimado debe ser mayor que 0.")
        return value

    def validate_distance(self, value: float) -> float:
        """
        Valida que la distancia sea mayor que 0.

        Args:
            value (float): Distancia estimada.

        Raises:
            serializers.ValidationError: Si la distancia no es válida.

        Returns:
            float: Distancia validada.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError("La distancia debe ser mayor que 0.")
        return value

    def validate(self, attrs: dict) -> dict:
        """
        Valida reglas de negocio entre estado y conductor.

        Args:
            attrs (dict): Atributos validados.

        Raises:
            serializers.ValidationError: Si la combinación de estado y conductor no es válida.

        Returns:
            dict: Atributos validados.
        """
        status = attrs.get('status')
        driver = attrs.get('driver')

        if status == 'completed' and driver is None:
            raise serializers.ValidationError("Un servicio completado debe tener un conductor asignado.")

        if status == 'pending' and driver is not None:
            raise serializers.ValidationError("Un servicio pendiente no debe tener un conductor asignado.")

        return attrs