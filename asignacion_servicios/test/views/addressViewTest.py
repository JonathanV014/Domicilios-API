from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from asignacion_servicios.models import Address


class AddressViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.address1 = Address.objects.create(
            name="Oficina Central",
            country="Colombia",
            city="Bogotá",
            street="Calle 1",
            latitude=4.60971,
            longitude=-74.08175
        )
        self.address2 = Address.objects.create(
            name="Sucursal",
            country="Colombia",
            city="Medellín",
            street="Calle 2",
            latitude=6.2442,
            longitude=-75.5812
        )
        self.list_url = reverse('addresses-list')

    def test_list_addresses(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_addresses_with_filters(self):
        response = self.client.get(self.list_url, {'country': 'Colombia', 'city': 'Bogotá'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Oficina Central")

    def test_create_address(self):
        data = {
            "name": "Nueva Oficina",
            "country": "Colombia",
            "city": "Cali",
            "street": "Calle 3",
            "latitude": 3.4516,
            "longitude": -76.5320
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 3)

    def test_create_address_duplicate(self):
        data = {
            "name": "Oficina Central",
            "country": "Colombia",
            "city": "Bogotá",
            "street": "Calle 1",
            "latitude": 4.60971,
            "longitude": -74.08175
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_retrieve_address(self):
        url = reverse('addresses-detail', args=[self.address1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Oficina Central")

    def test_retrieve_address_not_found(self):
        url = reverse('addresses-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_update_address(self):
        url = reverse('addresses-detail', args=[self.address1.id])
        data = {
            "name": "Oficina Actualizada",
            "country": "Colombia",
            "city": "Bogotá",
            "street": "Calle 1",
            "latitude": 4.60971,
            "longitude": -74.08175
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address1.refresh_from_db()
        self.assertEqual(self.address1.name, "Oficina Actualizada")

    def test_partial_update_address(self):
        url = reverse('addresses-detail', args=[self.address1.id])
        data = {"name": "Solo Nombre"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address1.refresh_from_db()
        self.assertEqual(self.address1.name, "Solo Nombre")

    def test_update_address_not_found(self):
        url = reverse('addresses-detail', args=[999])
        data = {"name": "No existe"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_destroy_address(self):
        url = reverse('addresses-detail', args=[self.address1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(id=self.address1.id).exists())

    def test_destroy_address_not_found(self):
        url = reverse('addresses-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_authentication_required(self):
        self.client.credentials()  
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)