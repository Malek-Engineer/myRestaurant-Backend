from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('customer', 'Customer'),
        ('driver', 'Driver'),
    ]

    email = models.EmailField(unique=True)
    wilaya = models.CharField(max_length=20)
    phone_number = models.IntegerField()

    def __str__(self): 
        return self.username
    

class RestaurantOwner:
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class RestaurantProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile_accounts')
    business_license_number = models.IntegerField()

    def __str__(self):
        return f"Restaurant: {self.user.username}"
    

class DriverProfile(models.Model):
    VEHICLE_CHOICES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
    ]
    VEHICLE_COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('gray', 'Gray'),
        ('silver', 'Silver'),
        ('brown', 'Brown'),
        ('orange', 'Orange'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    driver_license_number = models.IntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    vehicle_name = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=20)

    def __str__(self):
        return f"Driver: {self.user.username}"