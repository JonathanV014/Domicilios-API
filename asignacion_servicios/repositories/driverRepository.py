from django.db.models import QuerySet
from asignacion_servicios.models import Driver

class DriverRepository:
    @staticmethod
    def create(data: dict) -> Driver:
        return Driver.objects.create(**data)

    @staticmethod
    def get_by_id(driver_id):
        return Driver.objects.get(pk=driver_id)

    @staticmethod
    def list_all() -> QuerySet:
        return Driver.objects.all()

    @staticmethod
    def filter_by_status_city_country(is_available: bool, city: str, country: str) -> QuerySet:
        return Driver.objects.filter(
            is_available=is_available,
            address__city__iexact=city,
            address__country__iexact=country
        )

    @staticmethod
    def filter_by_status(is_available: bool) -> QuerySet:
        return Driver.objects.filter(is_available=is_available)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        return Driver.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        return Driver.objects.filter(**filters).exists()

    @staticmethod
    def update(driver: Driver, data: dict) -> Driver:
        for field, value in data.items():
            if hasattr(driver, field):
                setattr(driver, field, value)
        driver.save()
        return driver

    @staticmethod
    def delete(driver: Driver) -> None:
        driver.delete()