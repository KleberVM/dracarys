from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import render
import json
import os
# Importamos tus modelos
from api.models import Usuarios, UsuarioFacultad, Facultades

# Importamos el decorador de seguridad (asegúrate de tenerlo en decorators.py)
from .decorators import require_api_key

@csrf_exempt
@require_api_key
def obtener_usuario_por_parametro(request):
    """
    Busca un usuario recibiendo el SIS por la URL.
    Ejemplo: GET /api/usuarios/buscar/param/?sis=2026001
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Método no permitido. Usa GET.'}, status=405)

    sis = request.GET.get('sis')
    
    if not sis:
        return JsonResponse({'success': False, 'message': 'Falta el parámetro SIS en la URL'}, status=400)

    return _buscar_usuario_logica(sis)


@csrf_exempt
@require_api_key
def obtener_usuario_por_json(request):
    """
    Busca un usuario recibiendo el SIS dentro de un JSON.
    Ejemplo: POST /api/usuarios/buscar/json/ body: {"sis": "2026001"}
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido. Usa POST.'}, status=405)

    try:
        data = json.loads(request.body)
        sis = data.get('sis')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)

    if not sis:
        return JsonResponse({'success': False, 'message': 'Falta el campo SIS en el JSON'}, status=400)

    return _buscar_usuario_logica(sis)


def _buscar_usuario_logica(sis):
    """
    Función auxiliar privada para no repetir código.
    Busca al usuario y sus facultades.
    """
    usuario = Usuarios.objects.filter(sis=sis).first()

    if not usuario:
        return JsonResponse({'success': False, 'exists': False, 'message': 'Usuario no encontrado'}, status=404)

    # Búsqueda adicional: Obtener IDs y Nombres de las facultades del usuario
    facultades_ids = UsuarioFacultad.objects.filter(iduser=usuario).values_list('idfacultad__name', flat=True)
    
    datos_usuario = {
        #'iduser': usuario.iduser,
        'sis': usuario.sis,
        #'email': usuario.email,
        'nromaterias': usuario.nromaterias,
        'nrointentos': usuario.nrointentos,
        'enabled': usuario.enabled,
        'facultades': list(facultades_ids) # Devuelve ["Tecnología", "Economía"]
    }

    return JsonResponse({'success': True, 'exists': True, 'usuario': datos_usuario})

@csrf_exempt
@require_api_key
def crear_usuario(request):
    """
    Crea un usuario nuevo. Valida que el SIS no exista.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sis = data.get('sis')
            email = data.get('email', '')

            if not sis:
                return JsonResponse({'success': False, 'message': 'El SIS es obligatorio'}, status=400)

            if Usuarios.objects.filter(sis=sis).exists():
                return JsonResponse({'success': False, 'message': 'El usuario ya existe'}, status=409)

            nuevo_usuario = Usuarios.objects.create(
                sis=sis,
                email=email,
                nromaterias=data.get('nromaterias', 4),
                nrointentos=data.get('nrointentos', 0),
                enabled=data.get('enabled', False)
            )

            return JsonResponse({
                'success': True, 
                'message': 'Usuario creado', 
                'id': nuevo_usuario.iduser
            }, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
@require_api_key
def listar_usuarios(request):
    """
    Lista todos los usuarios básicos.
    """
    if request.method == 'GET':
        # values() es más rápido que traer objetos completos
        usuarios = list(Usuarios.objects.values('iduser', 'sis', 'email', 'enabled'))
        return JsonResponse({'success': True, 'cantidad': len(usuarios), 'usuarios': usuarios}, safe=False)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
@require_api_key
def eliminar_usuario(request):
    """
    Elimina un usuario por SIS (recibido por JSON).
    Automaticamente elimina sus relaciones en UsuarioFacultad por el CASCADE.
    """
    if request.method in ['DELETE', 'POST']:
        try:
            data = json.loads(request.body)
            sis = data.get('sis')

            if not sis:
                return JsonResponse({'success': False, 'message': 'Falta el SIS'}, status=400)

            usuario = Usuarios.objects.filter(sis=sis).first()

            if usuario:
                usuario.delete() # El CASCADE de SQL borrará inscripciones y facultades
                return JsonResponse({'success': True, 'message': f'Usuario {sis} eliminado correctamente'})
            else:
                return JsonResponse({'success': False, 'message': 'Usuario no encontrado'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
@require_api_key
def asignar_facultad(request):
    """
    Función extra: Asigna un usuario existente a una facultad existente.
    Recibe: {"sis": "...", "id_facultad": 1}
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sis = data.get('sis')
            id_facultad = data.get('id_facultad')

            user = Usuarios.objects.filter(sis=sis).first()
            facultad = Facultades.objects.filter(idfacultad=id_facultad).first()

            if not user or not facultad:
                return JsonResponse({'success': False, 'message': 'Usuario o Facultad no encontrados'}, status=404)

            # Evitar duplicados
            obj, created = UsuarioFacultad.objects.get_or_create(
                iduser=user,
                idfacultad=facultad
            )

            if created:
                return JsonResponse({'success': True, 'message': 'Asignación creada'})
            else:
                return JsonResponse({'success': True, 'message': 'El usuario ya pertenecía a esta facultad'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
            
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


# api/views.py

@csrf_exempt
@require_api_key
def incrementar_intentos(request):
    """
    Suma +1 al contador de nrointentos de un usuario.
    Recibe: {"sis": "202103154"}
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Usa POST'}, status=405)
    
    try:
        data = json.loads(request.body)
        sis = data.get('sis')
        usuario = Usuarios.objects.filter(sis=sis).first()
        
        if usuario:
            usuario.nrointentos += 1
            usuario.save()
            return JsonResponse({'success': True, 'nrointentos': usuario.nrointentos})
        return JsonResponse({'success': False, 'message': 'No encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

def consola_pruebas(request):
    # Pasamos la API KEY al template para que el JavaScript pueda usarla
    context = {
        'api_key': os.environ.get('DRACARYS_API_KEY', 'clave-no-configurada'),
        'titulo': 'Consola de Verificación Dracarys - UMSS'
    }
    return render(request, 'api/prueba.html', context)