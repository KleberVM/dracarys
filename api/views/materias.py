from django.http import JsonResponse
from api.models import Materias

def listar_materias(request):
    materias = list(Materias.objects.values('idmateria', 'name', 'created_at'))
    return JsonResponse(materias, safe=False)