from django.test import TestCase
from asignacion_servicios.models import Driver, Address
from asignacion_servicios.repositories import DriverRepository

class DriverRepositoryTestCase(TestCase):
    def setUp(self):
        self.address1 = Address.objects.create(
            name="Terminal Norte",
            country="Colombia",
            city="Medellín",
            street="Calle 10 #20-30",
            latitude=6.2442,
            longitude=-75.5812
        )
        self.address2 = Address.objects.create(
            name="Terminal Sur",
            country="Colombia",
            city="Cali",
            street="Avenida 3 #45-67",
            latitude=3.4516,
            longitude=-76.5320
        )
        self.driver1 = Driver.objects.create(
            name="Pedro Ruiz",
            phone="+573001234567",
            address=self.address1,
            is_available=True
        )
        self.driver2 = Driver.objects.create(
            name="Ana Torres",
            phone="+573002345678",
            address=self.address2,
            is_available=False
        )

    def test_create_driver(self):
        data = {
            "name": "Carlos Gómez",
            "phone": "+573003456789",
            "address": self.address1,
            "is_available": True
        }
        driver = DriverRepository.create(data)
        self.assertEqual(driver.name, "Carlos Gómez", "El nombre del conductor no coincide.")
        self.assertTrue(driver.is_available, "El estado de disponibilidad no coincide.")

    def test_get_by_id(self):
        driver = DriverRepository.get_by_id(self.driver1.id)
        self.assertEqual(driver.name, "Pedro Ruiz", "El conductor obtenido por ID no es el esperado.")

    def test_list_all(self):
        drivers = DriverRepository.list_all()
        self.assertEqual(drivers.count(), 2, "El número de conductores listados no es correcto.")

    def test_filter_by(self):
        drivers = DriverRepository.filter_by(is_available=True)
        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers.first().name, "Pedro Ruiz")

    def test_exists(self):
        exists = DriverRepository.exists(phone="+573001234567")
        self.assertTrue(exists)

    def test_update_driver(self):
        data = {"name": "Pedro Actualizado"}
        updated_driver = DriverRepository.update(self.driver1, data)
        self.assertEqual(updated_driver.name, "Pedro Actualizado")

    def test_delete_driver(self):
        DriverRepository.delete(self.driver1)
        drivers = DriverRepository.list_all()
        self.assertEqual(drivers.count(), 1)