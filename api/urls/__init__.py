from django.urls import include, path

urlpatterns = [
    path("facultades/", include("api.urls.facultades")),
    path("usuarios/", include("api.urls.usuarios")),
    path("materias/", include("api.urls.materias")),
    path("tokens/", include("api.urls.tokens")),
    path("", include("api.urls.home")),
]
