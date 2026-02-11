from functools import wraps
from django.http import JsonResponse
from django.conf import settings

def require_api_key(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. Buscamos la llave en el encabezado (Header)
        # El estándar es usar 'X-API-KEY' o 'Authorization'
        api_key = request.headers.get('X-API-KEY')

        # 2. Verificamos si la llave existe y si es correcta
        if not api_key:
            return JsonResponse({'success': False, 'message': 'Usuario no autorizado'}, status=401)

        if api_key != settings.DRACARYS_API_KEY:
            return JsonResponse({'success': False, 'message': 'Usuario no autorizado'}, status=403)

        # 3. Si todo está bien, dejamos pasar a la vista original
        return view_func(request, *args, **kwargs)

    return _wrapped_view