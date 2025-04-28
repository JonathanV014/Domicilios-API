from django.db.models import QuerySet
from asignacion_servicios.models import Driver

class DriverRepository:
    """
    Repositorio para operaciones CRUD y consultas sobre el modelo Driver.
    """

    @staticmethod
    def create(data: dict) -> Driver:
        """
        Crea una nueva instancia de Driver.

        Args:
            data (dict): Diccionario con los datos del conductor.

        Returns:
            Driver: Instancia creada de Driver.
        """
        return Driver.objects.create(**data)

    @staticmethod
    def get_by_id(driver_id: int) -> Driver:
        """
        Obtiene un conductor por su ID.

        Args:
            driver_id (int): ID del conductor.

        Returns:
            Driver: Instancia de Driver correspondiente al ID.
        """
        return Driver.objects.get(pk=driver_id)

    @staticmethod
    def list_all() -> QuerySet:
        """
        Lista todos los conductores.

        Returns:
            QuerySet: QuerySet con todas las instancias de Driver.
        """
        return Driver.objects.all()

    @staticmethod
    def filter_by_status_city_country(is_available: bool, city: str, country: str) -> QuerySet:
        """
        Filtra conductores por disponibilidad, ciudad y país.

        Args:
            is_available (bool): Estado de disponibilidad.
            city (str): Ciudad del conductor.
            country (str): País del conductor.

        Returns:
            QuerySet: QuerySet con los conductores filtrados.
        """
        return Driver.objects.filter(
            is_available=is_available,
            address__city__iexact=city,
            address__country__iexact=country
        )

    @staticmethod
    def filter_by_status(is_available: bool) -> QuerySet:
        """
        Filtra conductores por disponibilidad.

        Args:
            is_available (bool): Estado de disponibilidad.

        Returns:
            QuerySet: QuerySet con los conductores filtrados.
        """
        return Driver.objects.filter(is_available=is_available)

    @staticmethod
    def filter_by(**filters) -> QuerySet:
        """
        Filtra conductores por campos arbitrarios.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            QuerySet: QuerySet con los conductores filtrados.
        """
        return Driver.objects.filter(**filters)

    @staticmethod
    def exists(**filters) -> bool:
        """
        Verifica si existe un conductor con los filtros dados.

        Args:
            **filters: Campos y valores para filtrar.

        Returns:
            bool: True si existe al menos una coincidencia, False en caso contrario.
        """
        return Driver.objects.filter(**filters).exists()

    @staticmethod
    def update(driver: Driver, data: dict) -> Driver:
        """
        Actualiza los campos de un conductor existente.

        Args:
            driver (Driver): Instancia de Driver a actualizar.
            data (dict): Diccionario con los campos y valores a actualizar.

        Returns:
            Driver: Instancia de Driver actualizada.
        """
        for field, value in data.items():
            if hasattr(driver, field):
                setattr(driver, field, value)
        driver.save()
        return driver

    @staticmethod
    def delete(driver: Driver) -> None:
        """
        Elimina un conductor.

        Args:
            driver (Driver): Instancia de Driver a eliminar.
        """
        driver.delete()