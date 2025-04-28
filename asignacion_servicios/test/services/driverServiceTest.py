from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from asignacion_servicios.models import Driver, Address
from asignacion_servicios.services import DriverService

class DriverServiceTestCase(TestCase):
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
            "address": self.address1.id,
            "is_available": True
        }
        driver = DriverService.create_driver(data)
        self.assertEqual(driver.name, "Carlos Gómez")
        self.assertEqual(driver.phone, "+573003456789")
        self.assertTrue(driver.is_available)

    def test_create_driver_duplicate_phone(self):
        data = {
            "name": "Otro",
            "phone": "+573001234567", 
            "address": self.address1.id,
            "is_available": True
        }
        with self.assertRaises(ValidationError):
            DriverService.create_driver(data)

    def test_create_driver_invalid_address(self):
        data = {
            "name": "Sin Dirección",
            "phone": "+573009876543",
            "address": 999, 
            "is_available": True
        }
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.create_driver(data)

    def test_get_driver(self):
        driver = DriverService.get_driver(self.driver1.id)
        self.assertEqual(driver.name, "Pedro Ruiz")

    def test_get_driver_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.get_driver(999)

    def test_list_drivers(self):
        drivers = DriverService.list_drivers()
        self.assertEqual(drivers.count(), 2)

    def test_list_drivers_by_status(self):
        drivers = DriverService.list_drivers({"is_available": True})
        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers.first().name, "Pedro Ruiz")

    def test_update_driver(self):
        data = {"name": "Pedro Actualizado"}
        updated_driver = DriverService.update_driver(self.driver1.id, data)
        self.assertEqual(updated_driver.name, "Pedro Actualizado")

    def test_update_driver_duplicate_phone(self):
        data = {"phone": "+573002345678"} 
        with self.assertRaises(ValidationError):
            DriverService.update_driver(self.driver1.id, data)

    def test_update_driver_invalid_address(self):
        data = {"address": 999}
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.update_driver(self.driver1.id, data)

    def test_update_driver_not_found(self):
        data = {"name": "No Existe"}
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.update_driver(999, data)

    def test_delete_driver(self):
        DriverService.delete_driver(self.driver1.id)
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.get_driver(self.driver1.id)

    def test_delete_driver_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            DriverService.delete_driver(999)