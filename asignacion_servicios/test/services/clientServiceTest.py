from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from asignacion_servicios.models import Client, Address
from asignacion_servicios.services import ClientService

class ClientServiceTestCase(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            name="Oficina Central",
            country="Colombia",
            city="Bogotá",
            street="Calle Falsa 123",
            latitude=4.60971,
            longitude=-74.08175
        )
        self.client1 = Client.objects.create(
            name="Juan Pérez",
            phone="+573001234567",
            email="juan.perez@example.com",
            address=self.address
        )
        self.client2 = Client.objects.create(
            name="Ana Gómez",
            phone="+573002345678",
            email="ana.gomez@example.com",
            address=self.address
        )

    def test_create_client(self):
        data = {
            "name": "Carlos López",
            "phone": "+573003456789",
            "email": "carlos.lopez@example.com",
            "address": self.address
        }
        client = ClientService.create_client(data)
        self.assertEqual(client.name, "Carlos López")
        self.assertEqual(client.phone, "+573003456789")
        self.assertEqual(client.email, "carlos.lopez@example.com")

    def test_create_client_duplicate_email(self):
        data = {
            "name": "Otro Cliente",
            "phone": "+573004567890",
            "email": "juan.perez@example.com",  
            "address": self.address
        }
        with self.assertRaises(ValidationError):
            ClientService.create_client(data)

    def test_create_client_duplicate_phone(self):
        data = {
            "name": "Otro Cliente",
            "phone": "+573001234567",  
            "email": "otro@email.com",
            "address": self.address
        }
        with self.assertRaises(ValidationError):
            ClientService.create_client(data)

    def test_get_client(self):
        client = ClientService.get_client(self.client1.id)
        self.assertEqual(client.name, "Juan Pérez")

    def test_get_client_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            ClientService.get_client(999)

    def test_list_clients(self):
        clients = ClientService.list_clients()
        self.assertEqual(clients.count(), 2)

    def test_update_client(self):
        data = {"name": "Juan Actualizado"}
        updated_client = ClientService.update_client(self.client1.id, data)
        self.assertEqual(updated_client.name, "Juan Actualizado")

    def test_update_client_duplicate_email(self):
        data = {"email": "ana.gomez@example.com"}  
        with self.assertRaises(ValidationError):
            ClientService.update_client(self.client1.id, data)

    def test_update_client_duplicate_phone(self):
        data = {"phone": "+573002345678"}  
        with self.assertRaises(ValidationError):
            ClientService.update_client(self.client1.id, data)

    def test_update_client_not_found(self):
        data = {"name": "No Existe"}
        with self.assertRaises(ObjectDoesNotExist):
            ClientService.update_client(999, data)

    def test_delete_client(self):
        ClientService.delete_client(self.client1.id)
        with self.assertRaises(ObjectDoesNotExist):
            ClientService.get_client(self.client1.id)

    def test_delete_client_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            ClientService.delete_client(999)