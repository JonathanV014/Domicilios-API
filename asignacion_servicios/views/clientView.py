from rest_framework import viewsets, status
from rest_framework.response import Response
from asignacion_servicios.serializers.clientSerializer import ClientSerializer
from asignacion_servicios.services.clientService import ClientService
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ClientService.list_clients()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            client = ClientService.create_client(serializer.validated_data)
            output = self.get_serializer(client)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            client = ClientService.get_client(pk)
            serializer = self.get_serializer(client)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": f"Cliente con ID {pk} no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            client = ClientService.get_client(pk)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(client, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            updated_client = ClientService.update_client(pk, serializer.validated_data)
            output = self.get_serializer(updated_client)
            return Response(output.data)
        except ValidationError as e:
            return Response({"error": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            client = ClientService.get_client(pk)
        except ObjectDoesNotExist:
            return Response({"error": f"Cliente con ID {pk} no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(client, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_client = ClientService.update_client(pk, serializer.validated_data)
            output = self.get_serializer(updated_client)
            return Response(output.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            ClientService.delete_client(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": f"Cliente con ID {pk} no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
