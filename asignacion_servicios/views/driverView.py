from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers import DriverSerializer, ServiceSerializer
from asignacion_servicios.services import DriverService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .jwt_config import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD sobre el modelo Driver.
    """
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], url_path='complete-service', permission_classes=[IsAuthenticated])
    def complete_service(self, request, pk=None):
        """
        Marca un servicio como completado por el conductor.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del conductor.

        Returns:
            Response: Respuesta HTTP con el servicio actualizado o error.
        """
        service_id = request.data.get('service_id')
        if not service_id:
            return Response({"error": "El ID del servicio es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = DriverService.complete_service(pk, service_id)
            return Response({"message": "Servicio marcado como completado.", "service": ServiceSerializer(service).data})
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        """
        Retorna el queryset de conductores, filtrando por disponibilidad, ciudad y país si se especifican.

        Returns:
            QuerySet: QuerySet de conductores filtrados.
        """
        filters = {
            'is_available': self.request.query_params.get('is_available'),
            'city': self.request.query_params.get('city'),
            'country': self.request.query_params.get('country')
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        return DriverService.list_drivers(filters)

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo conductor.

        Args:
            request (Request): Objeto de la petición HTTP.

        Returns:
            Response: Respuesta HTTP con el conductor creado o error de validación.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            driver = DriverService.create_driver(serializer.validated_data)
            output = self.get_serializer(driver)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"address": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            if hasattr(e, 'detail'):
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Recupera un conductor por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del conductor.

        Returns:
            Response: Respuesta HTTP con el conductor o error si no existe.
        """
        try:
            driver = DriverService.get_driver(pk)
            serializer = self.get_serializer(driver)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza un conductor existente.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del conductor.

        Returns:
            Response: Respuesta HTTP con el conductor actualizado o error de validación.
        """
        try:
            driver = DriverService.get_driver(pk)
            serializer = self.get_serializer(driver, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_driver = DriverService.update_driver(pk, serializer.validated_data)
            output = self.get_serializer(updated_driver)
            return Response(output.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            error_msg = e.message_dict if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza parcialmente un conductor existente.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del conductor.

        Returns:
            Response: Respuesta HTTP con el conductor actualizado o error de validación.
        """
        try:
            driver = DriverService.get_driver(pk)
            serializer = self.get_serializer(driver, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_driver = DriverService.update_driver(pk, serializer.validated_data)
            output = self.get_serializer(updated_driver)
            return Response(output.data)
        except ValidationError as e:
            error_msg = e.message_dict if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Elimina un conductor por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID del conductor.

        Returns:
            Response: Respuesta HTTP con estado 204 si se elimina correctamente o error si no existe.
        """
        try:
            DriverService.delete_driver(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
