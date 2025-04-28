from django.db.models import QuerySet
from asignacion_servicios.models import Address

class AddressRepository:
    """
    Repositorio para operaciones CRUD y consultas sobre el modelo Address.
    """

    @staticmethod
    def create(data: dict) -> Address:
        """
        Crea una nueva instancia de Address.

        Args:
            data (dict): Diccionario con los datos de la dirección.

        Returns:
            Address: Instancia creada de Address.
        """
        return Address.objects.create(**data)

    @staticmethod
    def get_by_id(address_id: int) -> Address:
        """
        Obtiene una dirección por su ID.

        Args:
            address_id (int): ID de la dirección.

        Returns:
            Address: Instancia de Address correspondiente al ID.
        """
        return Address.objects.get(pk=address_id)

    @staticmethod
    def list_all() -> QuerySet:
        """
        Lista todas las direcciones.

        Returns:
            QuerySet: QuerySet con todas las instancias de Address.
        """
        return Address.objects.all()

    @staticmethod
    def filter_by_country(country: str) -> QuerySet:
        """
        Filtra direcciones por país (case insensitive).

        Args:
            country (str): Nombre del país.

        Returns:
            QuerySet: QuerySet con las direcciones filtradas por país.
        """
        return Address.objects.filter(country__iexact=country)

    @staticmethod
    def filter_by_city(city: str) -> QuerySet:
        """
        Filtra direcciones por ciudad (case insensitive).

        Args:
            city (str): Nombre de la ciudad.

        Returns:
            QuerySet: QuerySet con las direcciones filtradas por ciudad.
        """
        return Address.objects.filter(city__iexact=city)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        """
        Filtra direcciones por campos arbitrarios.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            QuerySet: QuerySet con las direcciones filtradas.
        """
        return Address.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        """
        Verifica si existe una dirección con los filtros dados.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            bool: True si existe al menos una coincidencia, False en caso contrario.
        """
        return Address.objects.filter(**filters).exists()

    @staticmethod
    def update(address: Address, data: dict) -> Address:
        """
        Actualiza los campos de una dirección existente.

        Args:
            address (Address): Instancia de Address a actualizar.
            data (dict): Diccionario con los campos y valores a actualizar.

        Returns:
            Address: Instancia de Address actualizada.
        """
        for field, value in data.items():
            if hasattr(address, field):
                setattr(address, field, value)
        address.save()
        return address

    @staticmethod
    def delete(address: Address) -> None:
        """
        Elimina una dirección.

        Args:
            address (Address): Instancia de Address a eliminar.
        """
        address.delete()

    @staticmethod
    def get_with_related(address_id: int) -> Address:
        """
        Obtiene una dirección por su ID, incluyendo relaciones relacionadas.

        Args:
            address_id (int): ID de la dirección.

        Returns:
            Address: Instancia de Address con relaciones cargadas.
        """
        return Address.objects.select_related().get(pk=address_id)