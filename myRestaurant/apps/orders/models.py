from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from apps.accounts.models import User
from apps.restaurants.models import MenuItem


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def calculate_total_price(self):
        """
        Calculate the total price of the order based on its items.
        """
        total = sum(item.quantity * item.menu_item.price for item in self.items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        """
        Ensure the quantity is greater than 0.
        """
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('elDahabia', 'ElDahabia'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Set the paid_at field when the payment is marked as paid.
        """
        if self.is_paid and not self.paid_at:
            self.paid_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.method} ({'Paid' if self.is_paid else 'Unpaid'})"