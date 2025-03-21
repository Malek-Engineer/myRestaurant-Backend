from django.db import models
from apps.accounts.models import User
from datetime import datetime 


class Restaurant(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    address = models.CharField(max_length=100, unique=True)
    opening_hours = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    photos = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='restaurant_qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_Available(self):
        if not self.opening_hours: 
            return False
        
        try:
            # Parse the opening_hours field (e.g., "09:00-21:00")
            opening_time, closing_time = self.opening_hours.split('-')
            opening_time = datetime.strptime(opening_time, "%H:%M").time()
            closing_time = datetime.strptime(closing_time, "%H:%M").time()

            # Get the current time
            current_time = datetime.now().time()

            # Check if the current time is within the opening hours
            return opening_time <= current_time <= closing_time
        except ValueError:
            # If opening_hours is not in the correct format, return False
            return False

    def __str__(self):
        return f"Restaurant: {self.user.username} - {self.address}"
    

class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100)  # Define name as a CharField

    def __str__(self):
        return f"Menu: {self.name} ({self.restaurant.user.username})"

class Section(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"MenuItem: {self.name} ({self.section.name})"


