from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers import DriverSerializer, ServiceSerializer
from asignacion_servicios.services import DriverService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .jwt_config import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], url_path='complete-service', permission_classes=[IsAuthenticated])
    def complete_service(self, request, pk=None):
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
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        filters = {
            'is_available': self.request.query_params.get('is_available'),
            'city': self.request.query_params.get('city'),
            'country': self.request.query_params.get('country')
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        return DriverService.list_drivers(filters)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            driver = DriverService.get_driver(pk)
            serializer = self.get_serializer(driver)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            driver = DriverService.get_driver(pk)
            
            serializer = self.get_serializer(driver, data=request.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            updated = DriverService.update_driver(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            error_msg = e.message_dict if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            driver = DriverService.get_driver(pk)
            
            serializer = self.get_serializer(driver, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            updated = DriverService.update_driver(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data)
        except ValidationError as e:
            error_msg = e.message_dict if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            DriverService.delete_driver(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Driver with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
