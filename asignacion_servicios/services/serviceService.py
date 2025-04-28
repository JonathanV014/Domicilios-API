from asignacion_servicios.repositories.serviceRepository import ServiceRepository
from asignacion_servicios.models import Service, Driver, Address, Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from geopy.distance import geodesic


class ServiceService:

    @staticmethod
    def create_service(data):
        if 'client' not in data or not data['client']:
            raise ValidationError("El cliente es obligatorio para crear un servicio.")

        if 'pickup_address' in data and isinstance(data['pickup_address'], int):
            try:
                data['pickup_address'] = Address.objects.get(pk=data['pickup_address'])
            except Address.DoesNotExist:
                raise ObjectDoesNotExist(f"La dirección con ID {data['pickup_address']} no existe.")

        pickup_address = data['pickup_address']
        available_drivers = Driver.objects.filter(is_available=True, address__city=pickup_address.city)

        if not available_drivers.exists():
            raise ValidationError("No hay conductores disponibles en este momento.")

        pickup_coords = (pickup_address.latitude, pickup_address.longitude)
        closest_driver = None
        min_distance = float('inf')

        for driver in available_drivers:
            driver_coords = (driver.address.latitude, driver.address.longitude)
            distance = geodesic(pickup_coords, driver_coords).kilometers
            if distance < min_distance:
                min_distance = distance
                closest_driver = driver

        data['driver'] = closest_driver


        average_speed_kmh = 40 
        estimated_time = (min_distance / average_speed_kmh) * 60 

        data['distance'] = min_distance
        data['estimated_time'] = estimated_time

        if 'client' in data and isinstance(data['client'], int):
            try:
                data['client'] = Client.objects.get(pk=data['client'])
            except Client.DoesNotExist:
                raise ObjectDoesNotExist(f"El cliente con ID {data['client']} no existe.")

        service = ServiceRepository.create(data)

        return service

    @staticmethod
    def get_service(service_id):
        try:
            return ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

    @staticmethod
    def list_services(filters: dict = None) -> QuerySet[Service]:
        if filters and filters.get('status'):
            return ServiceRepository.filter_by_status(filters['status'])
        return ServiceRepository.list_all()

    @staticmethod
    def update_service(service_id, data):
        try:
            service = ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")

        if 'pickup_address' in data and isinstance(data['pickup_address'], int):
            try:
                data['pickup_address'] = Address.objects.get(pk=data['pickup_address'])
            except Address.DoesNotExist:
                raise ObjectDoesNotExist(f"La dirección con ID {data['pickup_address']} no existe.")

        if 'driver' in data and data['driver'] is not None:
            driver_instance = data['driver']
            if isinstance(driver_instance, int):
                try:
                    driver_instance = Driver.objects.get(pk=driver_instance)
                    data['driver'] = driver_instance
                except Driver.DoesNotExist:
                    raise ObjectDoesNotExist(f"El conductor con ID {data['driver']} no existe.")
            
            if not driver_instance.is_available:
                raise ValidationError("El conductor no está disponible.")

        if 'client' in data and isinstance(data['client'], int):
            try:
                data['client'] = Client.objects.get(pk=data['client'])
            except Client.DoesNotExist:
                raise ObjectDoesNotExist(f"El cliente con ID {data['client']} no existe.")

        return ServiceRepository.update(service, data)

    @staticmethod
    def delete_service(service_id):
        try:
            service = ServiceRepository.get_by_id(service_id)
        except Service.DoesNotExist:
            raise ObjectDoesNotExist(f"El servicio con ID {service_id} no existe.")
        ServiceRepository.delete(service)

    @staticmethod
    def calculate_distance(pickup_address: Address, destination_address: Address) -> float:

        pickup_coords = (pickup_address.latitude, pickup_address.longitude)
        destination_coords = (destination_address.latitude, destination_address.longitude)
        return geodesic(pickup_coords, destination_coords).kilometers
