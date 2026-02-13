# api/views/__init__.py

from .facultades import listar_facultades, crear_facultad
from .usuarios import listar_usuarios,obtener_usuario_por_parametro, obtener_usuario_por_json, crear_usuario, eliminar_usuario, asignar_facultad, incrementar_intentos, consola_pruebas
from .materias import listar_materias,materias_por_facultad_id, materias_por_facultad_nombre
from .home import home_dracarys