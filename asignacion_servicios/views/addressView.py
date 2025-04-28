from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers.addressSerializer import AddressSerializer
from asignacion_servicios.services.addressService import AddressService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class AddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD sobre el modelo Address.

    Métodos:
        get_queryset(): Permite filtrar direcciones por país y ciudad.
        create(): Crea una nueva dirección.
        retrieve(): Recupera una dirección por su ID.
        update(): Actualiza una dirección existente.
        partial_update(): Actualiza parcialmente una dirección existente.
        destroy(): Elimina una dirección por su ID.
    """
    serializer_class = AddressSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Obtiene el queryset de direcciones, filtrando opcionalmente por país y ciudad.

        Returns:
            QuerySet: QuerySet de direcciones filtradas o todas si no hay filtros.
        """
        filters = {
            'country': self.request.query_params.get('country'),
            'city': self.request.query_params.get('city')
        }
        filters = {k: v for k, v in filters.items() if v}
        return AddressService.list_addresses(filters)

    def create(self, request, *args, **kwargs):
        """
        Crea una nueva dirección.

        Args:
            request (Request): Objeto de la petición HTTP.

        Returns:
            Response: Respuesta HTTP con la dirección creada o error de validación.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            address = AddressService.create_address(serializer.validated_data)
            return Response(self.get_serializer(address).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Recupera una dirección por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID de la dirección.

        Returns:
            Response: Respuesta HTTP con la dirección o error si no existe.
        """
        try:
            address = AddressService.get_address(pk)
            return Response(self.get_serializer(address).data)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza una dirección existente.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID de la dirección.

        Returns:
            Response: Respuesta HTTP con la dirección actualizada o error de validación.
        """
        try:
            address = AddressService.get_address(pk)
            serializer = self.get_serializer(address, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_address = AddressService.update_address(pk, serializer.validated_data)
            return Response(self.get_serializer(updated_address).data)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Actualiza parcialmente una dirección existente.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID de la dirección.

        Returns:
            Response: Respuesta HTTP con la dirección actualizada o error de validación.
        """
        try:
            address = AddressService.get_address(pk)
            serializer = self.get_serializer(address, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_address = AddressService.update_address(pk, serializer.validated_data)
            return Response(self.get_serializer(updated_address).data)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Elimina una dirección por su ID.

        Args:
            request (Request): Objeto de la petición HTTP.
            pk (int, optional): ID de la dirección.

        Returns:
            Response: Respuesta HTTP con estado 204 si se elimina correctamente o error si no existe.
        """
        try:
            AddressService.delete_address(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
