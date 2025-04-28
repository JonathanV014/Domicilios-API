from asignacion_servicios.repositories import ClientRepository
from asignacion_servicios.models import Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet

class ClientService:

    @staticmethod
    def create_client(data: dict) -> Client:
        if ClientRepository.exists(email=data.get('email')):
            raise ValidationError("El correo electrónico ya está registrado.")
        if ClientRepository.exists(phone=data.get('phone')):
            raise ValidationError("El número de teléfono ya está registrado.")

        return ClientRepository.create(data)

    @staticmethod
    def get_client(client_id):
        try:
            return ClientRepository.get_by_id(client_id)
        except Client.DoesNotExist:
            raise ObjectDoesNotExist(f"El cliente con ID {client_id} no existe.")

    @staticmethod
    def list_clients() -> QuerySet[Client]:
        return ClientRepository.list_all()

    @staticmethod
    def update_client(client_id, data):
        try:
            client = ClientRepository.get_by_id(client_id)
        except Client.DoesNotExist:
            raise ObjectDoesNotExist(f"El cliente con ID {client_id} no existe.")

        if 'email' in data and Client.objects.filter(email=data['email']).exclude(pk=client_id).exists():
            raise ValidationError("Ya existe un cliente con este email.")

        if 'phone' in data and Client.objects.filter(phone=data['phone']).exclude(pk=client_id).exists():
            raise ValidationError("Ya existe un cliente con este teléfono.")

        for field, value in data.items():
            setattr(client, field, value)
        client.save()
        return client

    @staticmethod
    def delete_client(client_id: int) -> None:
        try:
            client = ClientRepository.get_by_id(client_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"El cliente con ID {client_id} no existe.")

        ClientRepository.delete(client)
