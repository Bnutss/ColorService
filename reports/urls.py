from django.urls import path
from reports import views


urlpatterns = [
    path('get_data/', views.get_data_color_service),
]