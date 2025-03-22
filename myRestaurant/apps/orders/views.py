from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new order and calculate the total price.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order.calculate_total_price()  # Calculate total price after saving
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update the status of an order.
        """
        order = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'completed', 'canceled']:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status
        order.save()
        return Response(self.get_serializer(order).data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing order items.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Add an item to an order and recalculate the total price.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()
        order_item.order.calculate_total_price()  # Recalculate total price
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing payments.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a payment for an order.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        if payment.is_paid:
            payment.paid_at = now()
            payment.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)