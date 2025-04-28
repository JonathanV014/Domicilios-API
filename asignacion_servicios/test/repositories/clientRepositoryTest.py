from django.test import TestCase
from asignacion_servicios.models import Client, Address
from asignacion_servicios.repositories import ClientRepository

class ClientRepositoryTestCase(TestCase):
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

        self.client1 = Client.objects.create(
            name="Juan Pérez",
            phone="+573001234567",
            email="juan.perez@example.com",
            address=self.address1
        )
        self.client2 = Client.objects.create(
            name="María Gómez",
            phone="+573002345678",
            email="maria.gomez@example.com",
            address=self.address2
        )

    def test_create_client(self):
        data = {
            "name": "Carlos López",
            "phone": "+573003456789",
            "email": "carlos.lopez@example.com",
            "address": self.address1
        }
        client = ClientRepository.create(data)
        self.assertEqual(client.name, "Carlos López")
        self.assertEqual(client.phone, "+573003456789")
        self.assertEqual(client.email, "carlos.lopez@example.com")

    def test_get_by_id(self):
        client = ClientRepository.get_by_id(self.client1.id)
        self.assertEqual(client.name, "Juan Pérez")

    def test_list_all(self):
        clients = ClientRepository.list_all()
        self.assertEqual(clients.count(), 2)

    def test_filter_by(self):
        clients = ClientRepository.filter_by(name="Juan Pérez")
        self.assertEqual(clients.count(), 1)
        self.assertEqual(clients.first().email, "juan.perez@example.com")

    def test_exists(self):
        exists = ClientRepository.exists(email="juan.perez@example.com")
        self.assertTrue(exists)

    def test_update_client(self):
        data = {"name": "Juan Actualizado"}
        updated_client = ClientRepository.update(self.client1, data)
        self.assertEqual(updated_client.name, "Juan Actualizado")

    def test_delete_client(self):
        ClientRepository.delete(self.client1)
        clients = ClientRepository.list_all()
        self.assertEqual(clients.count(), 1)

    def test_get_with_related(self):
        client = ClientRepository.get_with_related(self.client1.id)
        self.assertEqual(client.name, "Juan Pérez")
        self.assertEqual(client.address.name, "Oficina Central")