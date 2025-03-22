import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from apps.accounts.models import User
from datetime import datetime


class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    address = models.CharField(max_length=100, unique=True) 
    opening_hours = models.CharField(max_length=10, blank=True, null=True)  #("09:00-21:00")
    description = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='restaurant_profile_photos/', blank=True, null=True)  
    qr_code = models.ImageField(upload_to='restaurant_qr_codes/', blank=True, null=True)  # QR Code field
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def is_available(self):
        """
        Check if the restaurant is currently open based on its opening hours.
        """
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

    def generate_qr_code(self):
        """
        Generate a QR code for the restaurant profile.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"https://myrestaurant.com/restaurants/{self.id}/"  # Example URL
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"restaurant_{self.id}_qr.png", File(buffer), save=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a QR code if it doesn't exist.
        """
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Restaurant: {self.user.username} - {self.address}"


class RestaurantPhoto(models.Model):
    """
    Model for additional photos published by the restaurant (e.g., food photos).
    """
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='restaurant_photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for the photo
    uploaded_at = models.DateTimeField(auto_now_add=True)  # when the photo was uploaded

    def __str__(self):
        return f"Photo for {self.restaurant.name} - {self.caption or 'No Caption'}"


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100) 

    def __str__(self):
        return f"Menu: {self.name} ({self.restaurant.user.username})"


class Section(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Section: {self.name} ({self.menu.name})"


class MenuItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    photo = models.ImageField(upload_to='menu_item_photos/', blank=True, null=True)

    def __str__(self):
        return f"MenuItem: {self.name} ({self.section.name})"