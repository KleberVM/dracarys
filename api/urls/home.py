from django.urls import path
from api import views # Importas tus vistas desde la carpeta api

urlpatterns = [
    path('', views.home_dracarys, name='home_dracarys'),
]