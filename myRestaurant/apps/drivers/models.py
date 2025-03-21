from django.db import models
from apps.orders.models import Order
from apps.accounts.models import User


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    is_available = models.BooleanField(default=False)
    assigned_orders = models.ManyToManyField(Order, related_name='driver', blank=True)

    def __str__(self):
        return f"Driver: {self.user.first_name} {self.user.last_name} ({'Available' if self.is_available else 'Unavailable'})"
    
    