from django.urls import path, include

urlpatterns = [
    path('facultades/', include('api.urls.facultades')),
    path('usuarios/', include('api.urls.usuarios')),
    path('materias/', include('api.urls.materias')),
    path('', include('api.urls.home')),
]
