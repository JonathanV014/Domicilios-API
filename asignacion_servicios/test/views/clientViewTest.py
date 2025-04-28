from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from asignacion_servicios.models import Client, Address


class ClientViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.address1 = Address.objects.create(
            name="Domicilio 1",
            country="España",
            city="Madrid",
            street="Calle Principal 1",
            latitude=40.416775,
            longitude=-3.703790
        )
        self.address2 = Address.objects.create(
            name="Domicilio 2",
            country="España",
            city="Barcelona",
            street="Calle Principal 2",
            latitude=41.385064,
            longitude=2.173403
        )

        self.client1 = Client.objects.create(
            name="Cliente Test 1",
            phone="+34611111111",
            email="cliente1@test.com",
            address=self.address1
        )
        self.client2 = Client.objects.create(
            name="Cliente Test 2",
            phone="+34622222222",
            email="cliente2@test.com",
            address=self.address2
        )

        self.list_url = reverse('clients-list')

    def test_list_clients(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_client_success(self):
        data = {
            "name": "Nuevo Cliente",
            "phone": "+34633333333",
            "email": "nuevo@test.com",
            "address": self.address1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 3)
        self.assertEqual(response.data['name'], "Nuevo Cliente")

    def test_create_client_invalid_email(self):
        data = {
            "name": "Cliente Duplicado",
            "phone": "+34644444444",
            "email": "cliente1@test.com",  
            "address": self.address1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_client_invalid_phone(self):
        data = {
            "name": "Cliente Teléfono Inválido",
            "phone": "no-es-telefono",
            "email": "telefonoinvalido@test.com",
            "address": self.address1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_client_invalid_name(self):
        data = {
            "name": "123456", 
            "phone": "+34655555555",
            "email": "nombreinvalido@test.com",
            "address": self.address1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_client_missing_address(self):
        data = {
            "name": "Cliente Sin Dirección",
            "phone": "+34666666666",
            "email": "sindireccion@test.com"
        
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_client(self):
        url = reverse('clients-detail', args=[self.client1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.client1.name)
        self.assertEqual(response.data['email'], self.client1.email)

    def test_retrieve_client_not_found(self):
        url = reverse('clients-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_update_client(self):
        url = reverse('clients-detail', args=[self.client1.id])
        data = {
            "name": "Cliente Actualizado",
            "phone": "+34677777777",
            "email": "actualizado@test.com",
            "address": self.address2.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.name, "Cliente Actualizado")
        self.assertEqual(self.client1.email, "actualizado@test.com")

    def test_partial_update_client(self):
        url = reverse('clients-detail', args=[self.client1.id])
        data = {"name": "Nombre Actualizado"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.name, "Nombre Actualizado")
        self.assertEqual(self.client1.email, "cliente1@test.com")  

    def test_update_client_not_found(self):
        url = reverse('clients-detail', args=[999])
        data = {"name": "No Existe"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_destroy_client(self):
        url = reverse('clients-detail', args=[self.client1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client1.id).exists())

    def test_destroy_client_not_found(self):
        url = reverse('clients-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_authentication_required(self):
        self.client.credentials()
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)