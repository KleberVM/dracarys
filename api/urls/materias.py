
from django.urls import path
from api.views.materias import listar_materias

urlpatterns = [
    path('', listar_materias),
]