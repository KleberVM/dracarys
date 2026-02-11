from django.urls import path
from api.views.facultades import listar_facultades, crear_facultad

urlpatterns = [
    
    path('', listar_facultades),      
    path('crear/', crear_facultad),
]