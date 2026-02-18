from django.urls import path

from api.views.tokens import actualizar_token, crear_token, listar_tokens, obtener_token

urlpatterns = [
    path("", listar_tokens),
    path("crear/", crear_token),
    path("<str:token_id>/", obtener_token),
    path("<str:token_id>/actualizar/", actualizar_token),
]
