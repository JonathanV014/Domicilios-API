from asignacion_servicios.repositories.serviceRepository import ServiceRepository
from asignacion_servicios.models import Service, Driver, Address, Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from geopy.distance import geodesic

class ServiceService:
    """
    Servicio para operaciones de negocio relacionadas con servicios.
    """

    @staticmethod
    def create_service(data: dict):
        """
        Crea un nuevo servicio, asignando el conductor más cercano si hay disponibles.

        Args:
            data (dict): Diccionario con los datos del servicio.

        Raises:
            ValidationError: Si falta el cliente o el conductor no está disponible.
            ObjectDoesNotExist: Si la dirección o el cliente no existen.

        Returns:
            tuple: (Service, warning) El servicio creado y advertencia si no hay conductores disponibles.
        """
        data = data.copy()
        if 'client' not in data or not data['client']:
            raise ValidationError("El cliente es obligatorio para crear un servicio.")

        data['pickup_address'] = ServiceService._get_instance(Address, data.get('pickup_address'), "La dirección")
        pickup_address = data['pickup_address']

        if 'driver' in data and data['driver'] is not None:
            driver_instance = ServiceService._get_instance(Driver, data['driver'], "El conductor")
            if not driver_instance.is_available:
                raise ValidationError("El conductor no está disponible.")
            data['driver'] = driver_instance
        else:
            closest_driver, min_distance = ServiceService._find_closest_driver(pickup_address)
            if closest_driver:
                closest_driver.is_available = False
                closest_driver.save()
                data['driver'] = closest_driver
                average_speed_kmh = 40
                estimated_time = (min_distance / average_speed_kmh) * 60
                data['distance'] = min_distance
                data['estimated_time'] = estimated_time
                warning = None
            else:
                data['driver'] = None
                data['distance'] = None
                data['estimated_time'] = None
                warning = "No hay conductores disponibles en este momento."

        data['client'] = ServiceService._get_instance(Client, data.get('client'), "El cliente")

        service = ServiceRepository.create(data)
        # Si se pasó un driver explícitamente, warning siempre será None
        if 'driver' in data and data['driver'] is not None:
            warning = None
        return service, warning

    @staticmethod
    def _find_closest_driver(pickup_address: Address):
        """
        Encuentra el conductor disponible más cercano a la dirección de recogida.

        Args:
            pickup_address (Address): Dirección de recogida.

        Returns:
            tuple: (Driver o None, distancia mínima o None)
        """
        available_drivers = Driver.objects.filter(is_available=True, address__city=pickup_address.city, address__country=pickup_address.country)
        pickup_coords = (pickup_address.latitude, pickup_address.longitude)
        closest_driver = None
        min_distance = None

        if available_drivers.exists():
            min_distance = float('inf')
            for driver in available_drivers:
                driver_coords = (driver.address.latitude, driver.address.longitude)
                distance = geodesic(pickup_coords, driver_coords).kilometers
                if distance < min_distance:
                    min_distance = distance
                    closest_driver = driver
            return closest_driver, min_distance
        return None, None

    @staticmethod
    def _get_instance(model, pk, label):
        """
        Obtiene una instancia de un modelo por su PK.

        Args:
            model (Model): Modelo Django.
            pk (int o instancia): PK o instancia del modelo.
            label (str): Nombre para el mensaje de error.

        Raises:
            ObjectDoesNotExist: Si la instancia no existe.

        Returns:
            Model: Instancia del modelo.
        """
        if isinstance(pk, int):
            try:
                return model.objects.get(pk=pk)
            except model.DoesNotExist:
                raise ObjectDoesNotExist(f"{label} con ID {pk} no existe.")
        return pk

    @staticmethod
    def get_service(service_id: int) -> Service:
        """
        Obtiene un servicio por su ID.

        Args:
            service_id (int): ID del servicio.

        Raises:
            ObjectDoesNotExist: Si el servicio no existe.

        Returns:
            Service: Instancia de Service correspondiente al ID.
        """
        try:
            return ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

    @staticmethod
    def list_services(filters: dict = None) -> QuerySet:
        """
        Lista servicios, opcionalmente filtrando por estado.

        Args:
            filters (dict, optional): Filtros de búsqueda.

        Returns:
            QuerySet: QuerySet de servicios.
        """
        if filters and filters.get('status'):
            return ServiceRepository.filter_by_status(filters['status'])
        return ServiceRepository.list_all()

    @staticmethod
    def update_service(service_id: int, data: dict) -> Service:
        """
        Actualiza los datos de un servicio existente.

        Args:
            service_id (int): ID del servicio.
            data (dict): Diccionario con los nuevos datos.

        Raises:
            ObjectDoesNotExist: Si el servicio, dirección, cliente o conductor no existen.
            ValidationError: Si el conductor no está disponible.

        Returns:
            Service: Instancia de Service actualizada.
        """
        try:
            service = ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

        data = data.copy()
        if 'pickup_address' in data:
            data['pickup_address'] = ServiceService._get_instance(Address, data['pickup_address'], "La dirección")

        if 'driver' in data and data['driver'] is not None:
            driver_instance = ServiceService._get_instance(Driver, data['driver'], "El conductor")
            if not driver_instance.is_available:
                raise ValidationError("El conductor no está disponible.")
            
            driver_instance.is_available = False
            driver_instance.save()
            data['driver'] = driver_instance

        if 'client' in data:
            data['client'] = ServiceService._get_instance(Client, data['client'], "El cliente")

        return ServiceRepository.update(service, data)

    @staticmethod
    def delete_service(service_id: int) -> None:
        """
        Elimina un servicio por su ID.

        Args:
            service_id (int): ID del servicio.

        Raises:
            ObjectDoesNotExist: Si el servicio no existe.
        """
        try:
            service = ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")
        ServiceRepository.delete(service)

    @staticmethod
    def calculate_distance(pickup_address: Address, destination_address: Address) -> float:
        """
        Calcula la distancia en kilómetros entre dos direcciones.

        Args:
            pickup_address (Address): Dirección de recogida.
            destination_address (Address): Dirección de destino.

        Returns:
            float: Distancia en kilómetros.
        """
        pickup_coords = (pickup_address.latitude, pickup_address.longitude)
        destination_coords = (destination_address.latitude, destination_address.longitude)
        return geodesic(pickup_coords, destination_coords).kilometers
