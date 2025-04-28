from rest_framework import serializers
from asignacion_servicios.models import Address

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Address.

    Valida que los campos obligatorios no estén vacíos, que las coordenadas sean válidas y que la dirección sea única.
    """

    class Meta:
        model = Address
        fields = ['id', 'name', 'country', 'city', 'street', 'latitude', 'longitude']
        read_only_fields = ['id']

    def _validate_not_empty(self, value, field_name):
        """
        Valida que un campo de texto no esté vacío.

        Args:
            value (str): Valor del campo.
            field_name (str): Nombre del campo para el mensaje de error.

        Raises:
            serializers.ValidationError: Si el campo está vacío.

        Returns:
            str: Valor validado.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(f"El campo '{field_name}' no puede estar vacío.")
        return value

    def validate_name(self, value):
        """
        Valida que el nombre no esté vacío.

        Args:
            value (str): Nombre de la dirección.

        Returns:
            str: Nombre validado.
        """
        return self._validate_not_empty(value, "nombre")

    def validate_country(self, value):
        """
        Valida que el país no esté vacío.

        Args:
            value (str): País de la dirección.

        Returns:
            str: País validado.
        """
        return self._validate_not_empty(value, "país")

    def validate_city(self, value):
        """
        Valida que la ciudad no esté vacía.

        Args:
            value (str): Ciudad de la dirección.

        Returns:
            str: Ciudad validada.
        """
        return self._validate_not_empty(value, "ciudad")

    def validate_latitude(self, value):
        """
        Valida que la latitud esté en el rango permitido.

        Args:
            value (float): Latitud.

        Raises:
            serializers.ValidationError: Si la latitud no está en el rango permitido.

        Returns:
            float: Latitud validada.
        """
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("La latitud debe estar entre -90 y 90 grados.")
        return value

    def validate_longitude(self, value):
        """
        Valida que la longitud esté en el rango permitido.

        Args:
            value (float): Longitud.

        Raises:
            serializers.ValidationError: Si la longitud no está en el rango permitido.

        Returns:
            float: Longitud validada.
        """
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("La longitud debe estar entre -180 y 180 grados.")
        return value

    def validate(self, attrs):
        """
        Valida que ambas coordenadas estén presentes o ninguna, y que la dirección sea única.

        Args:
            attrs (dict): Diccionario de atributos validados.

        Raises:
            serializers.ValidationError: Si solo una coordenada está presente o si la dirección ya existe.

        Returns:
            dict: Atributos validados.
        """
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
