from rest_framework import serializers
from .models import Restaurant, RestaurantPhoto, Menu, MenuItem, Section


class RestaurantPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantPhoto
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)  # Include menu items in the section

    class Meta:
        model = Section
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)  # Include sections in the menu

    class Meta:
        model = Menu
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source= 'user.username')
    profile_photo_url = serializers.ImageField(source='profile_photo', read_only=True)  # Profile photo URL
    qr_code_url = serializers.ImageField(source='qr_code', read_only=True)  # QR code URL

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'user',
            'restaurant_name',
            'address',
            'opening_hours',
            'description',
            'profile_photo_url',
            'qr_code_url',
            'created_at',
            'updated_at',
        ]