from django.test import TestCase
from asignacion_servicios.models import Service, Address, Client, Driver
from asignacion_servicios.repositories import ServiceRepository

class ServiceRepositoryTestCase(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            name="Oficina Central",
            country="Colombia",
            city="Bogotá",
            street="Calle Falsa 123",
            latitude=4.60971,
            longitude=-74.08175
        )
        self.client = Client.objects.create(
            name="Juan Pérez",
            phone="+573001234567",
            email="juan.perez@example.com",
            address=self.address
        )
        self.driver = Driver.objects.create(
            name="Pedro Ruiz",
            phone="+573001111111",
            address=self.address,
            is_available=True
        )
        self.service1 = Service.objects.create(
            pickup_address=self.address,
            client=self.client,
            driver=None,
            status="pending",
            estimated_time=30,
            distance=10
        )
        self.service2 = Service.objects.create(
            pickup_address=self.address,
            client=self.client,
            driver=self.driver,
            status="completed",
            estimated_time=25,
            distance=8
        )

    def test_create_service(self):
        data = {
            "pickup_address": self.address,
            "client": self.client,
            "driver": self.driver,
            "status": "in_progress",
            "estimated_time": 15,
            "distance": 5
        }
        service = ServiceRepository.create(data)
        self.assertEqual(service.status, "in_progress")
        self.assertEqual(service.driver, self.driver)

    def test_get_by_id(self):
        service = ServiceRepository.get_by_id(self.service1.id)
        self.assertEqual(service.status, "pending")

    def test_list_all(self):
        services = ServiceRepository.list_all()
        self.assertEqual(services.count(), 2)

    def test_filter_by_status(self):
        services = ServiceRepository.filter_by_status("completed")
        self.assertEqual(services.count(), 1)
        self.assertEqual(services.first().status, "completed")

    def test_filter_by(self):
        services = ServiceRepository.filter_by(client=self.client)
        self.assertEqual(services.count(), 2)

    def test_exists(self):
        exists = ServiceRepository.exists(status="pending")
        self.assertTrue(exists)

    def test_update_service(self):
        data = {"status": "canceled"}
        updated_service = ServiceRepository.update(self.service1, data)
        self.assertEqual(updated_service.status, "canceled")

    def test_delete_service(self):
        ServiceRepository.delete(self.service1)
        services = ServiceRepository.list_all()
        self.assertEqual(services.count(), 1)