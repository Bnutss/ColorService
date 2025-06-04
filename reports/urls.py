from django.urls import path
from .views import get_data_color_service


urlpatterns = [
    path('get_data/', get_data_color_service),
]