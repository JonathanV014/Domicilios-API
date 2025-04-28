from asignacion_servicios.repositories import DriverRepository, AddressRepository
from asignacion_servicios.models import Driver, Service
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class DriverService:
    """
    Servicio para operaciones de negocio relacionadas con conductores.
    """

    @staticmethod
    def create_driver(data: dict) -> Driver:
        """
        Crea un nuevo conductor.

        Args:
            data (dict): Diccionario con los datos del conductor.

        Raises:
            ObjectDoesNotExist: Si la dirección no existe.
            ValidationError: Si el teléfono ya está registrado.

        Returns:
            Driver: Instancia creada de Driver.
        """
        if 'address' in data and isinstance(data['address'], int):
            try:
                address = AddressRepository.get_by_id(data['address'])
                data = data.copy()
                data['address'] = address
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist(f"La dirección con ID {data['address']} no existe.")

        if 'phone' in data and Driver.objects.filter(phone=data['phone']).exists():
            raise ValidationError(f"Ya existe un conductor con el teléfono {data['phone']}")

        return DriverRepository.create(data)

    @staticmethod
    def complete_service(driver_id: int, service_id: int) -> Service:
        """
        Marca un servicio como completado por el conductor.

        Args:
            driver_id (int): ID del conductor.
            service_id (int): ID del servicio.

        Raises:
            ObjectDoesNotExist: Si el servicio no existe.
            ValidationError: Si el conductor no está asignado o el servicio no está en progreso.

        Returns:
            Service: Instancia de Service actualizada.
        """
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

        if service.driver is None or service.driver.id != int(driver_id):
            raise ValidationError("El conductor no está asignado a este servicio.")

        if service.status != 'in_progress':
            raise ValidationError("Solo se pueden completar servicios que estén en progreso.")

        service.status = 'completed'
        service.save()

        driver = service.driver
        driver.is_available = True
        driver.save()

        return service

    @staticmethod
    def assign_driver_to_service(driver_id: int, service_id: int) -> Service:
        """
        Asigna un conductor a un servicio.

        Args:
            driver_id (int): ID del conductor.
            service_id (int): ID del servicio.

        Raises:
            ObjectDoesNotExist: Si el conductor o el servicio no existen.

        Returns:
            Service: Instancia de Service actualizada.
        """
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

        try:
            driver = Driver.objects.get(pk=driver_id)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")

        service.driver = driver
        service.save()
        return service

    @staticmethod
    def get_driver(driver_id: int) -> Driver:
        """
        Obtiene un conductor por su ID.

        Args:
            driver_id (int): ID del conductor.

        Raises:
            ObjectDoesNotExist: Si el conductor no existe.

        Returns:
            Driver: Instancia de Driver correspondiente al ID.
        """
        try:
            return DriverRepository.get_by_id(driver_id)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")

    @staticmethod
    def list_drivers(filters: dict = None):
        """
        Lista conductores, opcionalmente filtrando por disponibilidad u otros campos.

        Args:
            filters (dict, optional): Diccionario de filtros.

        Returns:
            QuerySet: QuerySet con los conductores filtrados o todos si no hay filtros.
        """
        if filters is None:
            return DriverRepository.list_all()
        elif 'is_available' in filters and len(filters) == 1:
            return DriverRepository.filter_by_status(filters['is_available'])
        else:
            return DriverRepository.filter_by(**filters)

    @staticmethod
    def update_driver(driver_id: int, data: dict) -> Driver:
        """
        Actualiza los datos de un conductor existente.

        Args:
            driver_id (int): ID del conductor.
            data (dict): Diccionario con los nuevos datos.

        Raises:
            ObjectDoesNotExist: Si el conductor o la dirección no existen.
            ValidationError: Si el teléfono ya está registrado en otro conductor.

        Returns:
            Driver: Instancia de Driver actualizada.
        """
        try:
            driver = DriverRepository.get_by_id(driver_id)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")

        if 'address' in data and isinstance(data['address'], int):
            try:
                address = AddressRepository.get_by_id(data['address'])
                data = data.copy()
                data['address'] = address
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist(f"La dirección con ID {data['address']} no existe.")

        if 'phone' in data:
            if Driver.objects.filter(phone=data['phone']).exclude(pk=driver_id).exists():
                raise ValidationError(f"Ya existe un conductor con el teléfono {data['phone']}")

        return DriverRepository.update(driver, data)

    @staticmethod
    def delete_driver(driver_id: int) -> None:
        """
        Elimina un conductor por su ID.

        Args:
            driver_id (int): ID del conductor a eliminar.

        Raises:
            ObjectDoesNotExist: Si el conductor no existe.
        """
        try:
            driver = DriverRepository.get_by_id(driver_id)
            return DriverRepository.delete(driver)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")