from django.contrib import admin
from .models import Restaurant, Menu, Section, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'opening_hours')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('menu', 'name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('section', 'name', 'price', 'description')