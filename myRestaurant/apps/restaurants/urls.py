from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuViewSet, MenuItemViewSet, SectionViewSet, RestaurantPhotoViewSet

router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('menus', MenuViewSet, basename='menu')
router.register('menu-items', MenuItemViewSet, basename='menuitem')
router.register('sections', SectionViewSet, basename='section')
router.register('restaurant-photos', RestaurantPhotoViewSet, basename='restaurantphoto') 


urlpatterns = [
    path('', include(router.urls)),  # Include all registered routes
]