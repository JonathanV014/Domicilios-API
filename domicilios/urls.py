"""
URL configuration for domicilios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from asignacion_servicios.views import AddressViewSet, DriverViewSet, ClientViewSet, ServiceViewSet
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from django.views.generic.base import RedirectView


router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'drivers', DriverViewSet, basename='drivers')
router.register(r'services', ServiceViewSet, basename='services')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Domicilios API",
        default_version='v1',
        description="API para gestión de domicilios",
        contact=openapi.Contact(email="jonayma0110@gmal.com"),
        license=openapi.License(name="None"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('', RedirectView.as_view(url='/docs/', permanent=False), name='index'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls))
]
