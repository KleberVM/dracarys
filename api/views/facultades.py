from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Facultades # Fíjate que el import sigue igual
import json

def listar_facultades(request):
    facultades = list(Facultades.objects.values('idfacultad', 'name', 'created_at'))
    return JsonResponse(facultades, safe=False)

@csrf_exempt
def crear_facultad(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nueva = Facultades.objects.create(name=data.get('name'))
        return JsonResponse({'id': nueva.idfacultad, 'name': nueva.name})