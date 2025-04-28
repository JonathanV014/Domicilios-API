from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers import ServiceSerializer
from asignacion_servicios.services import ServiceService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD sobre el modelo Service.
    """
    serializer_class = ServiceSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna el queryset de servicios, filtrando por estado si se especifica.

        Returns:
            QuerySet: QuerySet de servicios filtrados.
        """
        filters = {'status': self.request.query_params.get('status')}
        filters = {k: v for k, v in filters.items() if v}
        return ServiceService.list_services(filters)


    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo servicio.

        Args:
            request (Request): Objeto de la petición HTTP.

        Returns:
            Response: Respuesta HTTP con el servicio creado o error de validación.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            service, warning = self._create_service_with_warning(serializer.validated_data)
            output = self.get_serializer(service)
            response_data = output.data
            if warning:
                response_data['warning'] = warning
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_service_with_warning(self, validated_data):
        """
        Llama a ServiceService.create_service y separa el warning si existe.

        Args:
            validated_data (dict): Datos validados del servicio.

        Returns:
            tuple: (Service, warning)
        """
        result = ServiceService.create_service(validated_data)
        if isinstance(result, tuple):
            return result
        return result, None

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Recupera un servicio por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del servicio.

        Returns:
            Response: Respuesta HTTP con el servicio o error si no existe.
        """
        try:
            service = ServiceService.get_service(pk)
            serializer = self.get_serializer(service)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": f"Service with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza completamente un servicio existente.

        Args:
            request (Request): Objeto de la petición HTTP con los datos a actualizar.
            pk (int, optional): ID del servicio a actualizar.

        Returns:
            Response: Respuesta HTTP con los datos actualizados del servicio o mensaje de error.
        """
        try:
            service = ServiceService.get_service(pk)
            serializer = self.get_serializer(service, data=request.data)
            # Esto lanzará ValidationError de DRF si el driver ID no existe
            serializer.is_valid(raise_exception=True)
            updated = ServiceService.update_service(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data)
        except ValidationError as e:
            # Devuelve directamente e.detail, que contiene el error formateado por DRF
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            error_msg = str(e)
            if "El servicio con ID" in error_msg:
                return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza parcialmente un servicio existente.
        
        Args:
            request (Request): Objeto de la petición HTTP con los datos a modificar.
            pk (int, optional): ID del servicio a actualizar parcialmente.

        Returns:
            Response: Respuesta HTTP con los datos actualizados del servicio o mensaje de error.
        """
        try:
            service = ServiceService.get_service(pk)
            serializer = self.get_serializer(service, data=request.data, partial=True)
            # Esto lanzará ValidationError de DRF si el driver ID no existe
            serializer.is_valid(raise_exception=True)
            updated = ServiceService.update_service(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data)
        except ValidationError as e:
            # Devuelve directamente e.detail, que contiene el error formateado por DRF
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            error_msg = str(e)
            if "El servicio con ID" in error_msg:
                return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
            # Para otros ObjectDoesNotExist (driver, address, client)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Considera loguear el error 'e' aquí para depuración
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Elimina un servicio por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del servicio.

        Returns:
            Response: Respuesta HTTP con estado 204 si se elimina correctamente o error si no existe.
        """
        try:
            ServiceService.delete_service(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Service with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
