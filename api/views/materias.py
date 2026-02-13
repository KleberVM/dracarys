from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Materias, Facultades

# Importamos tu decorador de seguridad
from .decorators import require_api_key

@csrf_exempt
@require_api_key
def listar_materias(request):
    """Lista todas las materias. Requiere API Key."""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    materias = list(Materias.objects.values('idmateria', 'name', 'created_at'))
    return JsonResponse({'success': True, 'materias': materias})


@csrf_exempt
@require_api_key
def materias_por_facultad_id(request):
    """
    Busca materias por ID de facultad vía parámetro GET.
    Ejemplo: GET /api/materias/por-id/?id=1
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Usa GET'}, status=405)

    id_facultad = request.GET.get('id')
    if not id_facultad:
        return JsonResponse({'success': False, 'message': 'Falta el parámetro id'}, status=400)

    # Validar que la facultad exista antes de filtrar
    if not Facultades.objects.filter(idfacultad=id_facultad).exists():
        return JsonResponse({'success': False, 'message': 'Facultad no encontrada'}, status=404)

    materias = list(Materias.objects.filter(idfacultad=id_facultad)
                    .values('idmateria', 'name'))
    
    return JsonResponse({'success': True, 'materias': materias})


@csrf_exempt
@require_api_key
def materias_por_facultad_nombre(request):
    """
    Busca materias por nombre de facultad.
    Ejemplo: GET /api/materias/por-nombre/?nombre=Tecnologia
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Usa GET'}, status=405)

    nombre = request.GET.get('nombre')
    if not nombre:
        return JsonResponse({'success': False, 'message': 'Falta el nombre de la facultad'}, status=400)

    # Filtramos materias usando la relación del nombre de la facultad (JOIN)
    materias = list(Materias.objects.filter(idfacultad__name__iexact=nombre)
                    .values('idmateria', 'name'))

    if not materias:
        return JsonResponse({'success': False, 'message': f'No hay materias para la facultad: {nombre}'}, status=404)

    return JsonResponse({'success': True, 'materias': materias})