from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_phone_number', 'is_available')  # Use helper methods for name and phone number
    list_filter = ('is_available',)
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number')  # Use double underscores to traverse relationships

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"  # Combine first and last name
    get_name.short_description = 'Name'  # Label for the admin panel

    def get_phone_number(self, obj):
        return obj.user.phone_number  # Assuming `phone_number` is a field in the User model
    get_phone_number.short_description = 'Phone Number'  # Label for the admin panel