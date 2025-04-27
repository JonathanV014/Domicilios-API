from django.db.models import QuerySet
from asignacion_servicios.models import Address

class AddressRepository:

    @staticmethod
    def create(data: dict) -> Address:
        return Address.objects.create(**data)

    @staticmethod
    def get_by_id(address_id):
        return Address.objects.get(pk=address_id)

    @staticmethod
    def list_all() -> QuerySet:
        return Address.objects.all()

    @staticmethod
    def filter_by_country(country: str) -> QuerySet:
        return Address.objects.filter(country__iexact=country)

    @staticmethod
    def filter_by_city(city: str) -> QuerySet:
        return Address.objects.filter(city__iexact=city)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        return Address.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        return Address.objects.filter(**filters).exists()

    @staticmethod
    def update(address, data):
        for field, value in data.items():
            setattr(address, field, value)
        address.save()
        return address

    @staticmethod
    def delete(address: Address) -> None:
        address.delete()

    @staticmethod
    def get_with_related(address_id: int) -> Address:
        return Address.objects.select_related().get(pk=address_id)