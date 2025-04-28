from asignacion_servicios.repositories import ClientRepository
from asignacion_servicios.models import Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet

class ClientService:
    """
    Servicio para operaciones de negocio relacionadas con clientes.
    """

    @staticmethod
    def create_client(data: dict) -> Client:
        """
        Crea un nuevo cliente si el email y el teléfono no están registrados.

        Args:
            data (dict): Diccionario con los datos del cliente.

        Raises:
            ValidationError: Si el email o el teléfono ya están registrados.

        Returns:
            Client: Instancia creada de Client.
        """
        if ClientRepository.exists(email=data.get('email')):
            raise ValidationError("El correo electrónico ya está registrado.")
        if ClientRepository.exists(phone=data.get('phone')):
            raise ValidationError("El número de teléfono ya está registrado.")

        return ClientRepository.create(data)

    @staticmethod
    def get_client(client_id: int) -> Client:
        """
        Obtiene un cliente por su ID.

        Args:
            client_id (int): ID del cliente.

        Raises:
            ObjectDoesNotExist: Si el cliente no existe.

        Returns:
            Client: Instancia de Client correspondiente al ID.
        """
        try:
            return ClientRepository.get_by_id(client_id)
        except Client.DoesNotExist:
            raise ObjectDoesNotExist(f"El cliente con ID {client_id} no existe.")

    @staticmethod
    def list_clients() -> QuerySet:
        """
        Lista todos los clientes.

        Returns:
            QuerySet: QuerySet con todas las instancias de Client.
        """
        return ClientRepository.list_all()

    @staticmethod
    def update_client(client_id: int, data: dict) -> Client:
        """
        Actualiza los datos de un cliente existente.

        Args:
            client_id (int): ID del cliente a actualizar.
            data (dict): Diccionario con los nuevos datos.

        Raises:
            ObjectDoesNotExist: Si el cliente no existe.
            ValidationError: Si el email o el teléfono ya están registrados en otro cliente.

        Returns:
            Client: Instancia de Client actualizada.
        """
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
        """
        Elimina un cliente por su ID.

        Args:
            client_id (int): ID del cliente a eliminar.

        Raises:
            ObjectDoesNotExist: Si el cliente no existe.
        """
        try:
            client = ClientRepository.get_by_id(client_id)
        except Client.DoesNotExist:
            raise ObjectDoesNotExist(f"El cliente con ID {client_id} no existe.")

        ClientRepository.delete(client)
