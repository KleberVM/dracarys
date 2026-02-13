from django.urls import path
from api.views.materias import (
    listar_materias, 
    materias_por_facultad_id, 
    materias_por_facultad_nombre
)

urlpatterns = [
    path('listar/', listar_materias),
    path('por-id/', materias_por_facultad_id),
    path('por-nombre/', materias_por_facultad_nombre),
]