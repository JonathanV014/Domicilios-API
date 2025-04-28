from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers.addressSerializer import AddressSerializer
from asignacion_servicios.services.addressService import AddressService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.permissions import IsAuthenticated

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filters = {
            'country': self.request.query_params.get('country'),
            'city': self.request.query_params.get('city')
        }
        filters = {k: v for k, v in filters.items() if v}
        return AddressService.list_addresses(filters)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            address = AddressService.create_address(serializer.validated_data)
            output = self.get_serializer(address)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            address = AddressService.get_address(pk)
            serializer = self.get_serializer(address)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            address = AddressService.get_address(pk)
            serializer = self.get_serializer(address, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated = AddressService.update_address(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            address = AddressService.get_address(pk)
            serializer = self.get_serializer(address, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated = AddressService.update_address(pk, serializer.validated_data)
            output = self.get_serializer(updated)
            return Response(output.data)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            AddressService.delete_address(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Address with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
