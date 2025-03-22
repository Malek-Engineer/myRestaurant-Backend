from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F
from .models import Driver
from apps.orders.models import Order
from .serializers import DriverSerializer, DriverAvailabilitySerializer


class DriverViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing drivers.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    @action(detail=True, methods=['patch'], url_path='update-availability')
    def update_availability(self, request, pk=None):
        """
        Update the availability of a driver.
        """
        driver = self.get_object()
        serializer = DriverAvailabilitySerializer(driver, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Driver availability updated successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='assign-order')
    def assign_order(self, request):
        pass 
    
    @action(detail=True, methods=['get'], url_path='assigned-orders')
    def assigned_orders(self, request, pk=None):
        """
        Retrieve all orders assigned to a specific driver.
        """
        driver = self.get_object()
        orders = driver.assigned_orders.all()
        return Response({'orders': [order.id for order in orders]}, status=status.HTTP_200_OK)