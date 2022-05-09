from django.urls import path

from .views import display_cart, add_to_cart, delete_from_cart

urlpatterns = [
    path('', display_cart, name="display_cart"),
    path('add/', add_to_cart, name="add_to_cart"),
    path('delete/', delete_from_cart, name="delete_from_cart"),
]