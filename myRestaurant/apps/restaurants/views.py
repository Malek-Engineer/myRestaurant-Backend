from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, RestaurantPhoto, Menu, MenuItem, Section
from .serializers import (
    RestaurantSerializer,
    RestaurantPhotoSerializer,
    MenuSerializer,
    MenuItemSerializer,
    SectionSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing restaurants.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantPhotoViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing restaurant photos.
    """
    queryset = RestaurantPhoto.objects.all()
    serializer_class = RestaurantPhotoSerializer

    def perform_create(self, serializer):
        """
        Automatically associate the photo with the authenticated user's restaurant.
        """
        restaurant = Restaurant.objects.get(user=self.request.user)
        serializer.save(restaurant=restaurant)


class MenuViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing menus.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def create(self, request, *args, **kwargs):
        """
        Ensure only one menu per restaurant.
        """
        restaurant_id = request.data.get('restaurant')
        if not restaurant_id:
            return Response({'error': 'The restaurant field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if Menu.objects.filter(restaurant_id=restaurant_id).exists():
            return Response({'error': 'A menu already exists for this restaurant.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)

    def update(self, request, *args, **kwargs):
        """
        Allow updating only the name of the menu.
        """
        # Ensure the request data is a dictionary
        if not isinstance(request.data, dict):
            return Response({'error': 'Invalid data format. Expected a JSON object.'}, status=status.HTTP_400_BAD_REQUEST)

        # Only allow updating the name
        name = request.data.get('name')
        if not name:
            return Response({'error': 'The name field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the name field only
        partial_data = {'name': name}
        serializer = self.get_serializer(self.get_object(), data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing sections.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def create(self, request, *args, **kwargs):
        """
        Ensure the menu exists before creating a section.
        """
        menu_id = request.data.get('menu')
        if not menu_id:
            return Response({'error': 'The menu field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Menu.objects.filter(id=menu_id).exists():
            return Response({'error': 'The specified menu does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)

    def update(self, request, *args, **kwargs):
        """
        Allow updating only the name of the section.
        """
        # Ensure the request data is a dictionary
        if not isinstance(request.data, dict):
            return Response({'error': 'Invalid data format. Expected a JSON object.'}, status=status.HTTP_400_BAD_REQUEST)

        # Only allow updating the name
        name = request.data.get('name')
        if not name:
            return Response({'error': 'The name field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the name field only
        partial_data = {'name': name}
        serializer = self.get_serializer(self.get_object(), data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a section.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Section deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing menu items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Ensure the section exists before creating a menu item.
        """
        section_id = request.data.get('section')
        if not section_id:
            return Response({'error': 'The section field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Section.objects.filter(id=section_id).exists():
            return Response({'error': 'The specified section does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)

    def update(self, request, *args, **kwargs):
        """
        Allow updating only the name, description, price, and photo of the menu item.
        """
        # Ensure the request data is a dictionary
        if not isinstance(request.data, dict):
            return Response({'error': 'Invalid data format. Expected a JSON object.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the specified fields
        partial_data = {}
        for field in ['name', 'description', 'price', 'photo']:
            if field in request.data:
                partial_data[field] = request.data[field]

        if not partial_data:
            return Response({'error': 'At least one field (name, description, price, or photo) is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(self.get_object(), data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)