from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from asignacion_servicios.models import Address, Client, Driver, Service

class ServiceViewSetTest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.address1 = Address.objects.create(
            name="Dirección 1", country="España", city="Madrid", 
            street="Calle Principal 1", latitude=40.416775, longitude=-3.703790
        )
        self.address2 = Address.objects.create(
            name="Dirección 2", country="España", city="Barcelona", 
            street="Calle Principal 2", latitude=41.385064, longitude=2.173403
        )

        self.client1 = Client.objects.create(
            name="Cliente Test 1", phone="+34611111111", 
            email="cliente1@test.com", address=self.address1
        )
        self.client2 = Client.objects.create(
            name="Cliente Test 2", phone="+34622222222", 
            email="cliente2@test.com", address=self.address2
        )
        
        self.driver_available = Driver.objects.create(
            name="Conductor Disponible", phone="+34633333333", 
            address=self.address1, is_available=True
        )
        self.driver_unavailable = Driver.objects.create(
            name="Conductor No Disponible", phone="+34644444444", 
            address=self.address2, is_available=False
        )
        
        self.service_pending = Service.objects.create(
            pickup_address=self.address1, client=self.client1
        )
        self.service_in_progress = Service.objects.create(
            pickup_address=self.address2, client=self.client2,
            driver=self.driver_available, status='in_progress', 
        )
        self.service_completed = Service.objects.create(
            pickup_address=self.address1, client=self.client1,
            driver=self.driver_available, status='completed', 
        )
        
        self.list_url = reverse('services-list')
    
    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_services(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
    
    def test_filter_services_by_status(self):
        response = self.client.get(f'{self.list_url}?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]['status'], 'pending')
        
        response = self.client.get(f'{self.list_url}?status=completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]['status'], 'completed')
    
    def test_create_service_success(self):
        self.driver_available.is_available = False
        self.driver_available.save()
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 4)
        self.assertEqual(response.data['status'], 'pending')
    
    def test_create_service_with_driver(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
            "driver": self.driver_available.id,
            "status": "in_progress",
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['driver'], self.driver_available.id)
    
    def test_create_service_unavailable_driver(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
            "driver": self.driver_unavailable.id,
            "status": "in_progress",
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_create_service_invalid_address(self):
        data = {
            "pickup_address": 999,  
            "client": self.client1.id,
            "status": "pending",
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_service_invalid_client(self):
        data = {
            "pickup_address": self.address1.id,
            "client": 999,  
            "status": "pending",
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_service_completed_no_driver(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
            "status": "completed",  
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_service_invalid_status(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
            "status": "invalid_status", 
            "estimated_time": 30.0,
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_service_negative_time(self):
        data = {
            "pickup_address": self.address1.id,
            "client": self.client1.id,
            "status": "pending",
            "estimated_time": -10.0, 
            "distance": 25.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_service(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.service_pending.id)
    
    def test_retrieve_nonexistent_service(self):
        url = reverse('services-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_update_service(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        data = {
            "pickup_address": self.address2.id,
            "client": self.client2.id,
            "driver": self.driver_available.id,
            "status": "in_progress",
            "estimated_time": 40.0,
            "distance": 30.0
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_pending.refresh_from_db()
        self.assertEqual(self.service_pending.status, "in_progress")
        self.assertEqual(self.service_pending.estimated_time, 40.0)
    
    def test_partial_update_service(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        data = {
            "estimated_time": 45.0,
            "distance": 35.0
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_pending.refresh_from_db()
        self.assertEqual(self.service_pending.estimated_time, 45.0)
        self.assertEqual(self.service_pending.distance, 35.0)

        self.assertEqual(self.service_pending.status, "pending")
    
    def test_update_service_assign_driver(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        data = {
            "driver": self.driver_available.id,
            "status": "in_progress"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_pending.refresh_from_db()
        self.assertEqual(self.service_pending.driver.id, self.driver_available.id)
        self.assertEqual(self.service_pending.status, "in_progress")
    
    def test_update_service_invalid_driver(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        data = {
            "driver": 999  
        }
        response = self.client.patch(url, data)
        self.assertIn("error", response.data)
    
    def test_update_nonexistent_service(self):
        url = reverse('services-detail', args=[999])
        data = {"status": "canceled"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_destroy_service(self):
        url = reverse('services-detail', args=[self.service_pending.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 2)
    
    def test_destroy_nonexistent_service(self):
        url = reverse('services-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)