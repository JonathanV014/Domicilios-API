from asignacion_servicios.repositories import AddressRepository
from asignacion_servicios.models import Address
from asignacion_servicios.serializers import AddressSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet

class AddressService:
    """
    Servicio para operaciones de negocio relacionadas con direcciones.
    """

    @staticmethod
    def create_address(data: dict) -> Address:
        """
        Crea una nueva dirección si no existe una igual.

        Args:
            data (dict): Diccionario con los datos de la dirección.

        Raises:
            ValidationError: Si los datos no son válidos o la dirección ya existe.

        Returns:
            Address: Instancia creada de Address.
        """
        serializer = AddressSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        if AddressRepository.exists(
            city=data.get('city'),
            country=data.get('country'),
            street=data.get('street'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        ):
            raise ValidationError("Esta dirección ya existe.")

        return AddressRepository.create(serializer.validated_data)

    @staticmethod
    def get_address(address_id: int) -> Address:
        """
        Obtiene una dirección por su ID.

        Args:
            address_id (int): ID de la dirección.

        Raises:
            ObjectDoesNotExist: Si la dirección no existe.

        Returns:
            Address: Instancia de Address correspondiente al ID.
        """
        try:
            return AddressRepository.get_by_id(address_id)
        except Address.DoesNotExist:
            raise ObjectDoesNotExist(f"La dirección con ID {address_id} no existe.")

    @staticmethod
    def list_addresses(filters: dict = None) -> QuerySet:
        """
        Lista direcciones, opcionalmente filtrando por país y/o ciudad.

        Args:
            filters (dict, optional): Diccionario con filtros de país y/o ciudad.

        Returns:
            QuerySet: QuerySet con las direcciones filtradas o todas si no hay filtros.
        """
        if not filters:
            return AddressRepository.list_all()

        country = filters.get('country')
        city = filters.get('city')

        if country and city:
            return AddressRepository.filter_by(country=country, city=city)
        if country:
            return AddressRepository.filter_by_country(country)
        if city:
            return AddressRepository.filter_by_city(city)

        return AddressRepository.list_all()

    @staticmethod
    def update_address(address_id: int, data: dict) -> Address:
        """
        Actualiza una dirección existente.

        Args:
            address_id (int): ID de la dirección a actualizar.
            data (dict): Diccionario con los nuevos datos.

        Raises:
            ObjectDoesNotExist: Si la dirección no existe.
            ValidationError: Si los datos no son válidos o la dirección actualizada sería duplicada.

        Returns:
            Address: Instancia de Address actualizada.
        """
        try:
            address = AddressRepository.get_by_id(address_id)
        except Address.DoesNotExist:
            raise ObjectDoesNotExist(f"La dirección con ID {address_id} no existe.")

        serializer = AddressSerializer(address, data=data, partial=True)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        unique_fields = ['city', 'country', 'street', 'latitude', 'longitude']
        if all(field in serializer.validated_data for field in unique_fields):
            filters = {field: serializer.validated_data[field] for field in unique_fields}
            if Address.objects.filter(**filters).exclude(pk=address_id).exists():
                raise ValidationError("Otra dirección con estos datos ya existe.")

        return AddressRepository.update(address, serializer.validated_data)

    @staticmethod
    def delete_address(address_id: int) -> None:
        """
        Elimina una dirección por su ID.

        Args:
            address_id (int): ID de la dirección a eliminar.

        Raises:
            ObjectDoesNotExist: Si la dirección no existe.
        """
        try:
            address = AddressRepository.get_by_id(address_id)
        except Address.DoesNotExist:
            raise ObjectDoesNotExist(f"La dirección con ID {address_id} no existe.")

        AddressRepository.delete(address)
