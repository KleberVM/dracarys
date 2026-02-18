from django.contrib import admin

from api.models import (
    Facultades,
    InscripcionDeseada,
    Materias,
    Tokens,
    UsuarioFacultad,
    Usuarios,
)


class FacultadInline(admin.TabularInline):
    model = UsuarioFacultad
    extra = 1
    verbose_name = "Facultad Asignada"
    verbose_name_plural = "Facultades del Estudiante"


class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
        "sis",
        "email",
        "nromaterias",
        "nrointentos",
        "enabled",
        "created_at",
    )

    search_fields = ("sis", "email")

    list_filter = ("enabled", "created_at")

    inlines = [FacultadInline]

    readonly_fields = ("created_at",)


class MateriasAdmin(admin.ModelAdmin):
    list_display = ("name", "idfacultad", "created_at")
    search_fields = ("name",)
    list_filter = ("idfacultad",)


class InscripcionDeseadaAdmin(admin.ModelAdmin):
    list_display = ("iduser", "idmateria", "grupo", "inscribir_cambiar", "created_at")
    search_fields = (
        "iduser__sis",
        "idmateria__name",
    )  # Busca por SIS del usuario o nombre de materia
    list_filter = ("inscribir_cambiar", "grupo")


class TokensAdmin(admin.ModelAdmin):
    list_display = ("token", "usos", "enabled", "created_at")
    search_fields = ("token",)
    list_filter = ("enabled", "created_at")
    readonly_fields = ("created_at",)


admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Facultades)
admin.site.register(Materias, MateriasAdmin)
admin.site.register(InscripcionDeseada, InscripcionDeseadaAdmin)
admin.site.register(Tokens, TokensAdmin)

# Opcional: Si quieres ver la tabla intermedia suelta, descomenta esto:
# admin.site.register(UsuarioFacultad)
