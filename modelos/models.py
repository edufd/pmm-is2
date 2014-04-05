from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    ci = models.IntegerField()
    username = models.CharField(max_length=200)
    telefono = models.IntegerField()
    contrasenha = models.CharField(max_length=200)
    class Meta:
        db_table = 'usuario'

class Rol(models.Model):
    id_rol = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    class Meta:
        db_table = 'rol'

class Permiso(models.Model):
    id_permiso = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    tipo = models.IntegerField()
    class Meta:
        db_table = 'permiso'

class UsuarioRol(models.Model):
    id_rol = models.ForeignKey('Rol')
    id_usuario = models.ForeignKey('Usuario')
    class Meta:
        db_table = 'usuario_rol'
        unique_together = (("id_rol", "id_usuario"),)

class RolPermiso(models.Model):
    id_rol = models.ForeignKey('Rol')
    id_permiso = models.ForeignKey('Permiso')
    class Meta:
        db_table = 'rol_permiso'
        unique_together = (("id_rol", "id_permiso"),)