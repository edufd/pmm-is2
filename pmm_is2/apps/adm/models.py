from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

FASES_ESTADOS = (
    ('NOINICIADA', 'NOINICIADA'),
    ('ABIERTA', 'ABIERTA'),
    ('FINALIZADA', 'FINALIZADA'),
    ('FINALIZADA', 'FINALIZADA'),
)

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=200, default='')
    apellido = models.CharField(max_length=200, default='')
    ci = models.IntegerField(unique=True)
    telefono = models.IntegerField()

    def __unicode__(self):
        return self.user.username

    # class Meta:
    #     db_table = 'userprofile'


class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200)
    presupuesto = models.IntegerField()
    costo_temporal = models.IntegerField()
    costo_monetario = models.IntegerField()
    estado = models.BooleanField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    plazo = models.IntegerField()

    def __unicode__(self):
        return self.nombre_proyecto

    class Meta:
        #db_table = 'proyecto'
        app_label = 'adm'


class UsuarioProyecto(models.Model):
    id_usuario_proyecto = models.AutoField(primary_key=True)
    #roles
    roles_proyecto = models.ManyToManyField(Group)
    proyectos = models.ForeignKey(Proyecto, related_name='usuario_proyecto')
    usuario_proyecto = models.ForeignKey(User)


class Fase(models.Model):
    id_fase = models.AutoField(primary_key=True)
    nombre_fase = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    id_proyecto = models.ManyToManyField(Proyecto)
    class Meta:
        #db_table = 'fase'
        app_label = 'adm'


