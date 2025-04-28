import random
from django.core.management.base import BaseCommand
from faker import Faker
from asignacion_servicios.models import Address, Driver

COLOMBIAN_CITIES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Cúcuta", "Bucaramanga",
    "Pereira", "Santa Marta", "Ibagué", "Villavicencio", "Manizales", "Neiva", "Pasto",
    "Armenia", "Montería", "Sincelejo", "Popayán", "Valledupar", "Tunja"
]

class Command(BaseCommand):
    help = 'Generar datos ficticios de Drivers y Services.'

    def handle(self, *args, **options):
        print("Generando datos...")
        self.generate_drivers_with_addresses(n=30)
        print("¡Datos generados con éxito!")

    def generate_address(self, faker):
        city = random.choice(COLOMBIAN_CITIES)
        return Address.objects.create(
            name=faker.company(),
            country="Colombia",
            city=city,
            street=faker.street_name(),
            latitude=faker.local_latlng(country_code="CO", coords_only=True)[0],
            longitude=faker.local_latlng(country_code="CO", coords_only=True)[1]
        )

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
