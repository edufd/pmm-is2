from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

ITEM_ESTADOS = (
    ('INACTIVO', 'INACTIVO'),
    ('BLOQUEADO', 'BLOQUEADO'),
    ('REVISION', 'REVISION'),
    ('ACTIVO', 'ACTIVO'),
    ('APROBADO', 'APROBADO'),
)

PRIORIDAD_CHOICES = (
    ('ALTA', 'ALTA'),
    ('MEDIA', 'MEDIA'),
    ('BAJA', 'BAJA'),
)

TIPO_ATRIBUTO = (
    ('NUMERICO', 'NUMERICO'),
    ('TEXTO', 'TEXTO'),
)

OBLIGATORIO = (
    ('NO', 'NO'),
    ('SI', 'SI'),
)

RELACION_TIPO = (
    ('PADRE-HIJO', 'PADRE-HIJO'),
    ('ANTECESOR-SUCESOR', 'ANTECESOR-SUCESOR'),
)


class Atributo(models.Model):
    id_atributo = models.AutoField(primary_key=True)
    nombre_atributo_tipo_item = models.CharField(max_length=200, unique=True, verbose_name="Nombre del Atributo")
    tipo_atributo = models.CharField(max_length=50, verbose_name="Tipo de Atributo")#N:NUMERICO #T:TEXTO
    obligatorio = models.CharField(max_length=50)#Y:OBLIGATORIO #N;NO ES OBLIGATORIO
    detalle = models.CharField(max_length=200)
    observacion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.detalle


class TipoItem(models.Model):
    id_tipo_item = models.AutoField(primary_key=True)
    nombre_tipo_item = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200)
    atributo = models.ForeignKey(Atributo, null=True)

    def __unicode__(self):
        return self.nombre_tipo_item


class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre_item = models.CharField(unique=False, max_length=200)
    version_item = models.IntegerField(blank=True)
    prioridad = models.CharField(max_length=5, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=10, choices=ITEM_ESTADOS, default='ACTIVO')
    descripcion = models.CharField(max_length=200)
    numero = models.CharField(max_length=200, blank=True, default='1')
    observaciones = models.CharField(max_length=5000)
    complejidad = models.IntegerField(max_length=10)
    costo = models.IntegerField()
    ultima_version_item_id = models.IntegerField(blank=True)
    id_tipo_item = models.ForeignKey(TipoItem, verbose_name="Tipo de Item")
    id_fase = models.ForeignKey('adm.Fase', verbose_name="Fase")
    modificado = models.ForeignKey(User)
    fecha_modificacion = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.nombre_item

    def relacion_padre_hijo(self):
        return self.ItemA.filter(esta_activa=True, tipo='PADRE-HIJO')

    def relacion_hijo_padre(self):
        return self.ItemB.filter(esta_activa=True, tipo='PADRE-HIJO')

    def save(self):
        existe = False
        existe = Item.objects.filter(id_item=self.id_item).exists()
        if existe is True:
            self.version_item = self.version_item + 1
            self.ultima_version_item_id = self.version_item
        else:
            self.version_item = 1
            self.ultima_version_item_id = 1

        super(Item, self).save()
        return Item


class VersionItem(models.Model):
    id_version_item = models.AutoField(primary_key=True)
    item_id = models.IntegerField()
    nombre_item = models.CharField(unique=False, max_length=200)
    version_item = models.IntegerField(blank=True)
    prioridad = models.CharField(max_length=5) #Alta:'A', Media:'M', Baja:'B'
    estado = models.CharField(max_length=10) # I:Inactivo  B:Bloqueado C:Revision A:Aprobado D:Desaprobado
    descripcion = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=5000)
    complejidad = models.IntegerField(max_length=10)
    costo = models.IntegerField()
    ultima_version_item_id = models.IntegerField(blank=True)
    id_tipo_item = models.ForeignKey(TipoItem, verbose_name="Tipo de Item")
    id_fase = models.ForeignKey('adm.Fase', verbose_name="Fase")
    modificado = models.ForeignKey(User)
    fecha_modificacion = models.DateTimeField(default=datetime.now())


class Relacion (models.Model):
    del_item = models.ForeignKey(Item, related_name="ItemA")
    al_item = models.ForeignKey(Item, related_name="ItemB")
    tipo = models.CharField(max_length=20, choices=RELACION_TIPO)
    fase = models.ForeignKey('adm.Fase', related_name='fases')
    esta_activa = models.BooleanField(default=True)

    class Meta:
        unique_together = (("del_item", "al_item", "tipo", "fase"),)


class ArchivoAdjunto(models.Model):
    id_archivo_adjunto = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    path_archivo = models.FileField(upload_to='documents/%Y%m%d')
    id_item_relacionado = models.ForeignKey(Item, related_name='archivo_adjunto')
    id_version_item = models.IntegerField()


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
    id_solicitud = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(blank=True, default=datetime.now())
    nombre_proyecto = models.ForeignKey('adm.Proyecto', verbose_name="Proyecto", null=True)
    nombre_fase = models.ForeignKey('adm.Fase', verbose_name="Fase", null=True)
    nombre_item = models.ForeignKey('des.Item', verbose_name="Item", null=True)
    usuario = models.ForeignKey(User, null=True)
    estado = models.CharField(max_length=11, default='EN-ESPERA')
    prioridad = models.CharField(max_length=5) #Alta:'A', Media:'M', Baja:'B'
    comentarios = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=5000)
    nombre_linea_base = models.ForeignKey('gdc.LineaBase', verbose_name="LineaBase", null=True)
    tipo = models.ManyToManyField(Tipo)
    opciones = models.ForeignKey(opciones, null=True)
    contador = models.IntegerField(blank=True, default=0, null=True)
    encontra = models.IntegerField(blank=True, default=0, null=True)

    votado_por1 = models.CharField(max_length=200, default='null', null=True)
    votado_por2 = models.CharField(max_length=200, default='null', null=True)
    votado_por3 = models.CharField(max_length=200, default='null', null=True)