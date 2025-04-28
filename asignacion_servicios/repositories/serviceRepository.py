from django.db.models import QuerySet
from asignacion_servicios.models import Service

class ServiceRepository:
    """
    Repositorio para operaciones CRUD y consultas sobre el modelo Service.
    """

    @staticmethod
    def create(data: dict) -> Service:
        """
        Crea una nueva instancia de Service.

        Args:
            data (dict): Diccionario con los datos del servicio.

        Returns:
            Service: Instancia creada de Service.
        """
        return Service.objects.create(**data)

    @staticmethod
    def get_by_id(service_id: int) -> Service:
        """
        Obtiene un servicio por su ID.

        Args:
            service_id (int): ID del servicio.

        Returns:
            Service: Instancia de Service correspondiente al ID.
        """
        return Service.objects.get(pk=service_id)

    @staticmethod
    def list_all() -> QuerySet:
        """
        Lista todos los servicios.

        Returns:
            QuerySet: QuerySet con todas las instancias de Service.
        """
        return Service.objects.all()

    @staticmethod
    def filter_by_status(status: str) -> QuerySet:
        """
        Filtra servicios por estado (case insensitive).

        Args:
            status (str): Estado del servicio.

        Returns:
            QuerySet: QuerySet con los servicios filtrados por estado.
        """
        return Service.objects.filter(status__iexact=status)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        """
        Filtra servicios por campos arbitrarios.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            QuerySet: QuerySet con los servicios filtrados.
        """
        return Service.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        """
        Verifica si existe un servicio con los filtros dados.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            bool: True si existe al menos una coincidencia, False en caso contrario.
        """
        return Service.objects.filter(**filters).exists()

    @staticmethod
    def update(service: Service, data: dict) -> Service:
        """
        Actualiza los campos de un servicio existente.

        Args:
            service (Service): Instancia de Service a actualizar.
            data (dict): Diccionario con los campos y valores a actualizar.

        Returns:
            Service: Instancia de Service actualizada.
        """
        for field, value in data.items():
            if hasattr(service, field):
                setattr(service, field, value)
        service.save()
        return service

    @staticmethod
    def delete(service: Service) -> None:
        """
        Elimina un servicio.

        Args:
            service (Service): Instancia de Service a eliminar.
        """
        service.delete()