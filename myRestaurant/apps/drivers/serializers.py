from rest_framework import serializers
from .models import Driver
from apps.orders.models import Order


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model.
    """
    assigned_orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = Driver
        fields = ['id', 'user', 'is_available', 'assigned_orders']


class DriverAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for updating driver availability.
    """
    class Meta:
        model = Driver
        fields = ['is_available']