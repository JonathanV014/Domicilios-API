from django.db.models import QuerySet
from asignacion_servicios.models import Client

class ClientRepository:

    @staticmethod
    def create(data: dict) -> Client:
        return Client.objects.create(**data)

    @staticmethod
    def get_by_id(client_id):
        return Client.objects.get(pk=client_id)
    
    @staticmethod
    def list_all() -> QuerySet:
        return Client.objects.all()

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        return Client.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        return Client.objects.filter(**filters).exists()

    @staticmethod
    def update(client: Client, data: dict) -> Client:
        for field, value in data.items():
            if hasattr(client, field):
                setattr(client, field, value)
        client.save()
        return client

    @staticmethod
    def delete(client: Client) -> None:
        client.delete()

    @staticmethod
    def get_with_related(client_id: int) -> Client:
        return Client.objects.select_related('address').get(pk=client_id)