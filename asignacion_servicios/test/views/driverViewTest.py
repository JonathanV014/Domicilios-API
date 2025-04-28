from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from asignacion_servicios.models import Address, Driver

class DriverViewSetTest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.address1 = Address.objects.create(
            name="Base 1", country="España", city="Madrid", street="Calle 1",
            latitude=40.416775, longitude=-3.703790
        )
        self.address2 = Address.objects.create(
            name="Base 2", country="España", city="Barcelona", street="Calle 2",
            latitude=41.385064, longitude=2.173403
        )

        self.driver1 = Driver.objects.create(
            name="Juan Pérez", phone="+34611111111", address=self.address1, is_available=True
        )
        self.driver2 = Driver.objects.create(
            name="Ana López", phone="+34622222222", address=self.address2, is_available=False
        )

        self.list_url = reverse('drivers-list')

    def test_list_drivers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_drivers_by_availability(self):
        response = self.client.get(self.list_url, {'is_available': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d['is_available'] for d in response.data))

    def test_create_driver_success(self):
        data = {
            "name": "Nuevo Conductor",
            "phone": "+34633333333",
            "address": self.address1.id,
            "is_available": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 3)
    
    def test_create_driver_duplicate_phone(self):
        data = {
            "name": "Otro Conductor",
            "phone": self.driver1.phone,
            "address": self.address2.id,
            "is_available": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)

    def test_create_driver_invalid_phone(self):
        data = {
            "name": "Conductor Inválido",
            "phone": "123",
            "address": self.address1.id,
            "is_available": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_driver_address_not_found(self):
        data = {
            "name": "Sin Dirección",
            "phone": "+34644444444",
            "address": 999,
            "is_available": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_driver(self):
        url = reverse('drivers-detail', args=[self.driver1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.driver1.name)

    def test_retrieve_driver_not_found(self):
        url = reverse('drivers-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_update_driver(self):
        url = reverse('drivers-detail', args=[self.driver1.id])
        data = {
            "name": "Juan Actualizado",
            "phone": "+34655555555",
            "address": self.address2.id,
            "is_available": False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver1.refresh_from_db()
        self.assertEqual(self.driver1.name, "Juan Actualizado")
        self.assertEqual(self.driver1.is_available, False)

    def test_update_driver_duplicate_phone(self):
        url = reverse('drivers-detail', args=[self.driver1.id])
        data = {
            "name": "Juan Actualizado",
            "phone": self.driver2.phone,  # Teléfono duplicado
            "address": self.address1.id,
            "is_available": True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_driver_not_found(self):
        url = reverse('drivers-detail', args=[999])
        data = {
            "name": "No Existe",
            "phone": "+34699999999",
            "address": self.address1.id,
            "is_available": True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_partial_update_driver(self):
        url = reverse('drivers-detail', args=[self.driver1.id])
        data = {"name": "Solo Nombre"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver1.refresh_from_db()
        self.assertEqual(self.driver1.name, "Solo Nombre")

    def test_destroy_driver(self):
        url = reverse('drivers-detail', args=[self.driver1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(id=self.driver1.id).exists())

    def test_destroy_driver_not_found(self):
        url = reverse('drivers-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.post(self.list_url, {
            "name": "Sin Auth",
            "phone": "+34688888888",
            "address": self.address1.id,
            "is_available": True
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)