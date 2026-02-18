import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Tokens

from .decorators import require_api_key


@csrf_exempt
@require_api_key
def obtener_token(request, token_id):
    """
    Obtiene información de un token específico y decrementa los usos
    """
    try:
        token = Tokens.objects.get(token=token_id)

        # Decrementar usos si es mayor que 0
        if token.enabled and token.usos > 0:
            token.usos -= 1
            token.save()

        data = {
            "token": token.token,
            "usos": token.usos,
            "enabled": token.enabled,
            "created_at": token.created_at,
        }
        return JsonResponse(data)
    except Tokens.DoesNotExist:
        return JsonResponse({"error": "Token no encontrado"}, status=404)


@csrf_exempt
@require_api_key
def listar_tokens(request):
    """
    Lista todos los tokens
    """
    tokens = list(Tokens.objects.values("token", "usos", "enabled", "created_at"))
    return JsonResponse(tokens, safe=False)


@csrf_exempt
@require_api_key
def crear_token(request):
    """
    Crea un nuevo token
    """
    if request.method == "POST":
        data = json.loads(request.body)
        token_value = data.get("token")

        if not token_value:
            return JsonResponse({"error": "El campo token es requerido"}, status=400)

        # Verificar si el token ya existe
        if Tokens.objects.filter(token=token_value).exists():
            return JsonResponse({"error": "El token ya existe"}, status=400)

        nuevo_token = Tokens.objects.create(
            token=token_value,
            usos=data.get("usos", 3),
            enabled=data.get("enabled", True),
        )

        return JsonResponse(
            {
                "token": nuevo_token.token,
                "usos": nuevo_token.usos,
                "enabled": nuevo_token.enabled,
                "created_at": nuevo_token.created_at,
            }
        )

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@require_api_key
def actualizar_token(request, token_id):
    """
    Actualiza información de un token (usos o enabled)
    """
    if request.method == "PUT":
        try:
            token = Tokens.objects.get(token=token_id)
            data = json.loads(request.body)

            if "usos" in data:
                token.usos = data["usos"]
            if "enabled" in data:
                token.enabled = data["enabled"]

            token.save()

            return JsonResponse(
                {
                    "token": token.token,
                    "usos": token.usos,
                    "enabled": token.enabled,
                    "created_at": token.created_at,
                }
            )
        except Tokens.DoesNotExist:
            return JsonResponse({"error": "Token no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)
