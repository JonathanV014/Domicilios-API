from django.db.models import QuerySet
from asignacion_servicios.models import Client

class ClientRepository:
    """
    Repositorio para operaciones CRUD y consultas sobre el modelo Client.
    """

    @staticmethod
    def create(data: dict) -> Client:
        """
        Crea una nueva instancia de Client.

        Args:
            data (dict): Diccionario con los datos del cliente.

        Returns:
            Client: Instancia creada de Client.
        """
        return Client.objects.create(**data)

    @staticmethod
    def get_by_id(client_id: int) -> Client:
        """
        Obtiene un cliente por su ID.

        Args:
            client_id (int): ID del cliente.

        Returns:
            Client: Instancia de Client correspondiente al ID.
        """
        return Client.objects.get(pk=client_id)
    
    @staticmethod
    def list_all() -> QuerySet:
        """
        Lista todos los clientes.

        Returns:
            QuerySet: QuerySet con todas las instancias de Client.
        """
        return Client.objects.all()

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        """
        Filtra clientes por campos arbitrarios.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            QuerySet: QuerySet con los clientes filtrados.
        """
        return Client.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        """
        Verifica si existe un cliente con los filtros dados.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            bool: True si existe al menos una coincidencia, False en caso contrario.
        """
        return Client.objects.filter(**filters).exists()

    @staticmethod
    def update(client: Client, data: dict) -> Client:
        """
        Actualiza los campos de un cliente existente.

        Args:
            client (Client): Instancia de Client a actualizar.
            data (dict): Diccionario con los campos y valores a actualizar.

        Returns:
            Client: Instancia de Client actualizada.
        """
        for field, value in data.items():
            if hasattr(client, field):
                setattr(client, field, value)
        client.save()
        return client

    @staticmethod
    def delete(client: Client) -> None:
        """
        Elimina un cliente.

        Args:
            client (Client): Instancia de Client a eliminar.
        """
        client.delete()

    @staticmethod
    def get_with_related(client_id: int) -> Client:
        """
        Obtiene un cliente por su ID, incluyendo la relación con Address.

        Args:
            client_id (int): ID del cliente.

        Returns:
            Client: Instancia de Client con la relación Address cargada.
        """
        return Client.objects.select_related('address').get(pk=client_id)