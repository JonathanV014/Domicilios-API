from asignacion_servicios.repositories import DriverRepository, AddressRepository
from asignacion_servicios.models import Driver, Service
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class DriverService:
    
    @staticmethod
    def create_driver(data):
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
    def complete_service(driver_id, service_id):
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
        return service
    
    @staticmethod
    def assign_driver_to_service(driver_id, service_id):
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
    def get_driver(driver_id):
        try:
            return DriverRepository.get_by_id(driver_id)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")
    
    @staticmethod
    def list_drivers(filters=None):
        if filters is None:
            return DriverRepository.list_all()
        elif 'is_available' in filters and len(filters) == 1:
            return DriverRepository.filter_by_status(filters['is_available'])
        else:
            return DriverRepository.filter_by(**filters)
    
    @staticmethod
    def update_driver(driver_id, data):
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
    def delete_driver(driver_id):
        try:
            driver = DriverRepository.get_by_id(driver_id)
            return DriverRepository.delete(driver)
        except Driver.DoesNotExist:
            raise ObjectDoesNotExist(f"El conductor con ID {driver_id} no existe.")