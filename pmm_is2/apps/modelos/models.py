from django.db import models

# Create your models here.
from django.db.models import ManyToManyField


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    ci = models.IntegerField()
    username = models.CharField(max_length=200)
    telefono = models.IntegerField()
    contrasenha = models.CharField(max_length=200)
    class Meta:
        db_table = 'usuario'

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    class Meta:
        db_table = 'rol'

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
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


class Subjects(models.Model):
    sub_name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
class Student(models.Model):
    name=models.CharField(max_length=100)
    subject=ManyToManyField(Subjects)
