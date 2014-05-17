from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


PRIORIDAD_CHOICES = (
    ('e','elegir...'),
    ('A', 'Alta'),
    ('M', 'Media'),
    ('B','Baja'),
)
# Cargar en la base de datos por defecto Ej> Nuevo Requerimiento > Cambio en requisito > Cambio en el disenho
class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    def __unicode__(self):
         return self.descripcion

# Cargar en la base de datos por defecto Ej> A favor > En contra >
class opciones(models.Model):
    id_opciones = models.AutoField(primary_key=True)
    opcion1 = models.CharField(max_length=15)
    def __unicode__(self):
         return self.opcion1

class Solicitud(models.Model):
    id_solicitud= models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(blank=True, default=datetime.now())
    nombre_proyecto=models.ForeignKey('adm.Proyecto', verbose_name="Proyecto",null=True)
    nombre_fase=models.ForeignKey('adm.Fase', verbose_name="Fase",null=True)
    nombre_item=models.ForeignKey('des.Item', verbose_name="Item",null=True)
    usuario=models.ForeignKey(User,null=True)
    estado = models.CharField(max_length=11, default='EN-ESPERA')
    prioridad = models.CharField(max_length=1) #Alta:'A', Media:'M', Baja:'B'
    comentarios = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=5000)
    nombre_linea_base=models.CharField(max_length=50, default='PRUEBA')#CAMBIAR DESPUES POR FOREINGNKEY CUANDO HAYA LB
    tipo = models.ManyToManyField(Tipo)
    opciones= models.ForeignKey(opciones, null=True)
    contador=models.IntegerField(blank=True,default=0,null=True)
    encontra=models.IntegerField(blank=True,default=0,null=True)
