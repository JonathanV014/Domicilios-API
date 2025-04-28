from django.test import TestCase
from asignacion_servicios.models import Address
from asignacion_servicios.repositories import AddressRepository

class AddressRepositoryTestCase(TestCase):
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
        self.address3 = Address.objects.create(
            name="Sucursal Sur",
            country="Colombia",
            city="Cali",
            street="Avenida Siempre Viva 742",
            latitude=3.4516,
            longitude=-76.5320
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
        address = AddressRepository.create(data)
        self.assertEqual(address.name, "Sucursal Este")
        self.assertEqual(address.city, "Barranquilla")

    def test_get_by_id(self):
        address = AddressRepository.get_by_id(self.address1.id)
        self.assertEqual(address.name, "Oficina Central")

    def test_list_all(self):
        addresses = AddressRepository.list_all()
        self.assertEqual(addresses.count(), 3)

    def test_filter_by_country(self):
        addresses = AddressRepository.filter_by_country("Colombia")
        self.assertEqual(addresses.count(), 3)

    def test_filter_by_city(self):
        addresses = AddressRepository.filter_by_city("Bogotá")
        self.assertEqual(addresses.count(), 1)
        self.assertEqual(addresses.first().name, "Oficina Central")

    def test_update_address(self):
        data = {"name": "Oficina Principal"}
        updated_address = AddressRepository.update(self.address1, data)
        self.assertEqual(updated_address.name, "Oficina Principal")

    def test_delete_address(self):
        AddressRepository.delete(self.address1)
        addresses = AddressRepository.list_all()
        self.assertEqual(addresses.count(), 2)

    def test_exists(self):
        exists = AddressRepository.exists(city="Bogotá", country="Colombia")
        self.assertTrue(exists)

    def test_get_with_related(self):
        address = AddressRepository.get_with_related(self.address1.id)
        self.assertEqual(address.name, "Oficina Central")