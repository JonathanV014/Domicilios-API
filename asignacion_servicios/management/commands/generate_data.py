from django.core.management.base import BaseCommand
from faker import Faker
from asignacion_servicios.models import Client, Address, Driver, Service

class Command(BaseCommand):
    help = 'Genera datos ficticios de Clients, Drivers y Services.'

    def handle(self, *args, **options):
        print("Generando datos...")
        
        self.generate_clients_with_addresses(n=50)


        self.generate_drivers_with_addresses(n=30)

        print("¡Datos generados con éxito!")

    def generate_address(self, faker):
        return Address.objects.create(
            name=faker.company(),
            country="Colombia",
            city=faker.city(),  
            street=faker.street_name(),
            latitude=faker.local_latlng(country_code="CO", coords_only=True)[0],
            longitude=faker.local_latlng(country_code="CO", coords_only=True)[1]
        )

    def generate_clients_with_addresses(self, n: int = 10):
        faker = Faker('es_CO')  

        for _ in range(n):
            address = self.generate_address(faker)  
            client = Client.objects.create(
                name=faker.name(),
                phone=faker.phone_number(),
                email=faker.email(),
                address=address
            )
           
            Service.objects.create(
                pickup_address=address,
                client=client,
                status="pending"
            )

        print(f"{n} clientes y sus direcciones generados.")

    def generate_drivers_with_addresses(self, n: int = 10):

        faker = Faker('es_CO')  

        for _ in range(n):
            address = self.generate_address(faker)  
            Driver.objects.create(
                name=faker.name(),
                phone=faker.phone_number(),
                address=address,
                is_available=faker.boolean()
            )

        print(f"{n} conductores y sus direcciones generados.")
