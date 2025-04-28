from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from asignacion_servicios.models import Address
from asignacion_servicios.services.addressService import AddressService

class AddressServiceTestCase(TestCase):
    def setUp(self):
        self.address1 = Address.objects.create(
            name="Oficina Central",
            country="Colombia",
            city="Bogotá",
            street="Calle Falsa 123",
            latitude=4.60971,
            longitude=-74.08175
        )
        self.address2 = Address.objects.create(
            name="Sucursal Norte",
            country="Colombia",
            city="Medellín",
            street="Carrera 45 #12-34",
            latitude=6.2442,
            longitude=-75.5812
        )

    def test_create_address(self):
        data = {
            "name": "Sucursal Este",
            "country": "Colombia",
            "city": "Barranquilla",
            "street": "Calle 84 #45-67",
            "latitude": 10.96854,
            "longitude": -74.78132
        }
        address = AddressService.create_address(data)
        self.assertEqual(address.name, "Sucursal Este")
        self.assertEqual(address.city, "Barranquilla")

    def test_create_address_duplicate(self):
        data = {
            "name": "Oficina Central",
            "country": "Colombia",
            "city": "Bogotá",
            "street": "Calle Falsa 123",
            "latitude": 4.60971,
            "longitude": -74.08175
        }
        with self.assertRaises(ValidationError):
            AddressService.create_address(data)

    def test_get_address(self):
        address = AddressService.get_address(self.address1.id)
        self.assertEqual(address.name, "Oficina Central")

    def test_get_address_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            AddressService.get_address(999)

    def test_list_addresses(self):
        addresses = AddressService.list_addresses()
        self.assertEqual(addresses.count(), 2)

    def test_list_addresses_with_filters(self):
        filters = {"country": "Colombia", "city": "Bogotá"}
        addresses = AddressService.list_addresses(filters)
        self.assertEqual(addresses.count(), 1)
        self.assertEqual(addresses.first().name, "Oficina Central")

    def test_update_address(self):
        data = {"name": "Oficina Principal"}
        updated_address = AddressService.update_address(self.address1.id, data)
        self.assertEqual(updated_address.name, "Oficina Principal")

    def test_update_address_not_found(self):
        data = {"name": "Nueva Dirección"}
        with self.assertRaises(ObjectDoesNotExist):
            AddressService.update_address(999, data)

    def test_delete_address(self):
        AddressService.delete_address(self.address1.id)
        with self.assertRaises(ObjectDoesNotExist):
            AddressService.get_address(self.address1.id)

    def test_delete_address_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            AddressService.delete_address(999)