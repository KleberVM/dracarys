from django.db import models
from django.db.models.functions import Now # Necesario para la fecha automática en SQL

class Facultades(models.Model):
    idfacultad = models.BigAutoField(primary_key=True, db_column='idFacultad')
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    
    # db_default=Now() -> Escribe "DEFAULT NOW()" en PostgreSQL
    created_at = models.DateTimeField(db_default=Now(), auto_now_add=True)

    class Meta:
        db_table = 'Facultades'
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'

    def __str__(self):
        return self.name or f"Facultad {self.idfacultad}"


class Usuarios(models.Model):
    iduser = models.BigAutoField(primary_key=True, db_column='idUser')
    sis = models.CharField(max_length=255, blank=True, null=False,unique=True)
    birthdate = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True, default='',db_default='')
    
    # db_default=False -> Escribe "DEFAULT false" en PostgreSQL
    enabled = models.BooleanField(db_default=False, default=False)
    
    created_at = models.DateTimeField(db_default=Now(), auto_now_add=True)
    
    # db_default=4 -> Escribe "DEFAULT 4" en PostgreSQL
    nromaterias = models.SmallIntegerField(db_column='nroMaterias', db_default=4, default=4)
    nrointentos = models.SmallIntegerField(db_column='nroIntentos', db_default=0, default=0)

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.sis} - {self.email}"


class Materias(models.Model):
    idmateria = models.BigAutoField(primary_key=True, db_column='idMateria')
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(db_default=Now(),auto_now_add=True)
    
    idfacultad = models.ForeignKey(
        Facultades, 
        models.CASCADE, 
        db_column='idFacultad', 
        blank=True, 
        null=True
    )

    class Meta:
        db_table = 'Materias'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def __str__(self):
        return self.name or f"Materia {self.idmateria}"


class UsuarioFacultad(models.Model):
    iduser_facultad = models.BigAutoField(primary_key=True, db_column='idUser_facultad')
    iduser = models.ForeignKey(Usuarios, models.CASCADE, db_column='idUser', blank=True, null=False)
    idfacultad = models.ForeignKey(Facultades, models.CASCADE, db_column='idFacultad', blank=True, null=False)
    created_at = models.DateTimeField(db_default=Now(), auto_now_add=True)

    class Meta:
        db_table = 'Usuario_Facultad'
        verbose_name = 'Usuario en Facultad'
        verbose_name_plural = 'Usuarios en Facultades'


class InscripcionDeseada(models.Model):
    idinscripcion = models.BigAutoField(primary_key=True, db_column='idInscripcion')
    iduser = models.ForeignKey(Usuarios, models.CASCADE, db_column='idUser', blank=True, null=True)
    idmateria = models.ForeignKey(Materias, models.CASCADE, db_column='idMateria', blank=True, null=True)
    
    grupo = models.CharField(max_length=255, blank=True, null=True)
    grupopractico = models.CharField(max_length=255, db_column='grupoPractico', blank=True, null=True)
    
    # db_default=True -> Escribe "DEFAULT true" en PostgreSQL
    inscribir_cambiar = models.BooleanField(db_default=True,default=True)
    created_at = models.DateTimeField(db_default=Now(), auto_now_add=True)

    class Meta:
        db_table = 'Inscripcion_deseada'
        verbose_name = 'Inscripción Deseada'
        verbose_name_plural = 'Inscripciones Deseadas'


class Tokens(models.Model):
    # llave primaria manual (No autoincremental)
    token = models.CharField(primary_key=True, max_length=255, db_column='token')
    
    usos = models.SmallIntegerField(db_default=3, default=3)

    enabled = models.BooleanField(db_default=True, default=True)

    created_at = models.DateTimeField(db_default=Now(), auto_now_add=True)

    class Meta:
        db_table = 'Tokens'
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def __str__(self):
        return f"Token: {self.token} (Usos restantes: {self.usos})"