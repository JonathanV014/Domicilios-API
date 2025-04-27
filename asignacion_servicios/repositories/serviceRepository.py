from django.db.models import QuerySet
from asignacion_servicios.models import Service

class ServiceRepository:

    @staticmethod
    def create(data: dict) -> Service:
        return Service.objects.create(**data)

    @staticmethod
    def get_by_id(service_id: int) -> Service:
        return Service.objects.get(pk=service_id)

    @staticmethod
    def list_all() -> QuerySet:
        return Service.objects.all()

    @staticmethod
    def filter_by_status(status: str) -> QuerySet:
        return Service.objects.filter(status__iexact=status)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        return Service.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        return Service.objects.filter(**filters).exists()

    @staticmethod
    def update(service: Service, data: dict) -> Service:
        for field, value in data.items():
            if hasattr(service, field):
                setattr(service, field, value)
        service.save()
        return service

    @staticmethod
    def delete(service: Service) -> None:
        service.delete()