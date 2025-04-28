from asignacion_servicios.repositories import AddressRepository
from asignacion_servicios.models import Address
from asignacion_servicios.serializers import AddressSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet

class AddressService:

    @staticmethod
    def create_address(data: dict) -> Address:

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
        try:
            return AddressRepository.get_by_id(address_id)
        except Address.DoesNotExist:
            raise ObjectDoesNotExist(f"La dirección con ID {address_id} no existe.")

    @staticmethod
    def list_addresses(filters: dict = None) -> QuerySet[Address]:
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
        try:
            address = AddressRepository.get_by_id(address_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"La dirección con ID {address_id} no existe.")

        AddressRepository.delete(address)
