from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from asignacion_servicios.models import Service, Client, Driver, Address
from asignacion_servicios.services import ServiceService

class ServiceServiceTestCase(TestCase):
    def setUp(self):
        self.address1 = Address.objects.create(
            name="Origen",
            country="Colombia",
            city="Bogotá",
            street="Calle 1 #2-3",
            latitude=4.60971,
            longitude=-74.08175
        )
        self.address2 = Address.objects.create(
            name="Destino",
            country="Colombia",
            city="Medellín",
            street="Carrera 10 #20-30",
            latitude=6.2442,
            longitude=-75.5812
        )
        self.client = Client.objects.create(
            name="Cliente Uno",
            phone="+573001234567",
            email="cliente@correo.com",
            address=self.address1
        )
        self.driver = Driver.objects.create(
            name="Conductor Uno",
            phone="+573009876543",
            address=self.address2,
            is_available=True
        )
        self.service = Service.objects.create(
            pickup_address=self.address1,
            client=self.client,
            driver=None,
            status="pending"
        )

    def test_create_service_ok(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client,
            "status": "pending"
        }
        service = ServiceService.create_service(data)
        self.assertEqual(service.status, "pending")
        self.assertEqual(service.pickup_address, self.address1)

    def test_create_service_without_client(self):
        data = {
            "pickup_address": self.address1.id,
            "status": "pending"
        }
        with self.assertRaises(ValidationError):
            ServiceService.create_service(data)

    def test_create_service_invalid_address(self):
        data = {
            "pickup_address": 999,
            "client": self.client,
            "status": "pending"
        }
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.create_service(data)

    def test_create_service_with_driver_not_available(self):
        self.driver.is_available = False
        self.driver.save()
        data = {
            "pickup_address": self.address1.id,
            "client": self.client,
            "driver": self.driver.id,
            "status": "in_progress"
        }
        with self.assertRaises(ValidationError):
            ServiceService.create_service(data)

    def test_create_service_with_driver_ok(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client,
            "driver": self.driver.id,
            "status": "in_progress"
        }
        service = ServiceService.create_service(data)
        self.assertEqual(service.driver, self.driver)

    def test_get_service(self):
        service = ServiceService.get_service(self.service.id)
        self.assertEqual(service.id, self.service.id)

    def test_get_service_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.get_service(999)

    def test_list_services(self):
        services = ServiceService.list_services()
        self.assertGreaterEqual(services.count(), 1)

    def test_list_services_with_status(self):
        services = ServiceService.list_services({"status": "pending"})
        self.assertTrue(all(s.status == "pending" for s in services))

    def test_update_service_ok(self):
        data = {"status": "in_progress", "driver": self.driver.id}
        updated = ServiceService.update_service(self.service.id, data)
        self.assertEqual(updated.status, "in_progress")
        self.assertEqual(updated.driver, self.driver)

    def test_update_service_invalid_driver(self):
        data = {"driver": 999}
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.update_service(self.service.id, data)

    def test_update_service_driver_not_available(self):
        self.driver.is_available = False
        self.driver.save()
        data = {"driver": self.driver.id}
        with self.assertRaises(ValidationError):
            ServiceService.update_service(self.service.id, data)

    def test_update_service_invalid_address(self):
        data = {"pickup_address": 999}
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.update_service(self.service.id, data)

    def test_update_service_not_found(self):
        data = {"status": "completed"}
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.update_service(999, data)

    def test_delete_service(self):
        service = ServiceService.create_service({
            "pickup_address": self.address1.id,
            "client": self.client,
            "status": "pending"
        })
        ServiceService.delete_service(service.id)
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.get_service(service.id)

    def test_delete_service_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            ServiceService.delete_service(999)

    def test_calculate_distance(self):
        distance = ServiceService.calculate_distance(self.address1, self.address2)
        self.assertTrue(distance > 0)