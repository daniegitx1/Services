from django.urls import path
from .views import service_list, add_listing

urlpatterns = [
    path('', service_list, name='service_list'),
    path('add/', add_listing, name='add_listing'),
]
