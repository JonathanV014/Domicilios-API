from django.contrib import admin

# Register your models here.
from asignacion_servicios.models import Driver, Service, Client, Address

admin.site.register(Driver)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Address)

