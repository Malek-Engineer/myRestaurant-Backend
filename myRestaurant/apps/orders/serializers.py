from rest_framework import serializers
from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)  

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'menu_item_name', 'quantity']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    """
    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'amount', 'is_paid', 'paid_at']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model, including related items and payment.
    """
    items = OrderItemSerializer(many=True, read_only=True)  # Include order items
    payment = PaymentSerializer(read_only=True)  # Include payment details
    customer_name = serializers.CharField(source='customer.username', read_only=True)  # Include customer name
    restaurant_name = serializers.CharField(source='restaurant.username', read_only=True)  # Include restaurant name

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'customer_name',
            'restaurant',
            'restaurant_name',
            'created_at',
            'updated_at',
            'total_price',
            'status',
            'items',
            'payment',
        ]