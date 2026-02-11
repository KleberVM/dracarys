# api/urls/usuarios.py
from django.urls import path
from api import views # Importas tus vistas desde la carpeta api

urlpatterns = [
    # Búsqueda por URL (GET)
    path('buscar/param/', views.usuarios.obtener_usuario_por_parametro, name='get_user_param'),
    
    # Búsqueda por JSON (POST)
    path('buscar/json/', views.usuarios.obtener_usuario_por_json, name='get_user_json'),
    
    # Gestión
    path('listar/', views.usuarios.listar_usuarios, name='list_users'),
    path('crear/', views.usuarios.crear_usuario, name='create_user'),
    path('eliminar/', views.usuarios.eliminar_usuario, name='delete_user'),
    path('asignar-facultad/', views.usuarios.asignar_facultad, name='assign_faculty'),
    path('incrementar/', views.usuarios.incrementar_intentos),
    path('consola/', views.usuarios.consola_pruebas, name='consola_pruebas'),
    
]