from django.db import models
from django.contrib.auth.models import User

ESTADO_CHOICES = (
    ('e','elegir...'),
    ('A', 'Aprobado'),
    ('N', 'No aprobado'),
)

PRIORIDAD_CHOICES = (
    ('e','elegir...'),
    ('A', 'Alta'),
    ('M', 'Media'),
    ('B','Baja'),
)

TIPO_ATRIBUTO = (
    ('e','elegir...'),
    ('N', 'NUMERICO'),
    ('T', 'TEXTO'),
)
OBLIGATORIO = (
    ('e','elegir...'),
    ('N','NO'),
    ('S','SI'),
)
TIPO = (
    ('e','elegir...'),
    ('P','Padre-hijo'),
    ('A','Antecesor-Sucesor'),
)

class TipoItem(models.Model):
    id_tipo_item = models.AutoField(primary_key=True)
    nombre_tipo_item = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nombre_tipo_item
    

class AtributoTipoItem(models.Model):
    id_atributo_tipo_item = models.AutoField(primary_key=True)
    id_tipo_item = models.ForeignKey('TipoItem')
    id_atributo = models.ForeignKey('Atributo')

class Atributo(models.Model):
    id_atributo = models.AutoField(primary_key=True)
    tipo_item = models.ForeignKey(TipoItem)
    nombre_atributo_tipo_item = models.CharField(max_length=200, unique=True, verbose_name="Nombre del Atributo")
    tipo_atributo = models.CharField(max_length=1, verbose_name="Tipo de Atributo")#N:NUMERICO #T:TEXTO
    obligatorio = models.CharField(max_length=1)#Y:OBLIGATORIO #N;NO ES OBLIGATORIO
    descripcion = models.CharField(max_length=200)
    observacion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.descripcion

class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre_item = models.CharField(unique=False, max_length=200)
    version_item = models.IntegerField(blank=True)
    prioridad = models.CharField(max_length=1) #Alta:'A', Media:'M', Baja:'B'
    estado = models.CharField(max_length=1) # I:Inactivo  B:Bloqueado C:Revision A:Aprobado D:Desaprobado
    descripcion = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=5000)
    complejidad = models.IntegerField(max_length=10)
    ultima_version_item_id = models.IntegerField(blank=True)
    id_tipo_item = models.ForeignKey(TipoItem, verbose_name="Tipo de Item")
    id_fase = models.ForeignKey('adm.Fase', verbose_name="Fase")

    def __unicode__(self):
        return self.nombre_item
    # class Meta:
    #      db_table = 'Item'

    def save(self):
        primera_version = False
        primera_version = Item.objects.filter(version_item=1).exists()
        if (primera_version is True):
            self.ultima_version_item_id = self.version_item
            self.version_item = self.version_item + 1
        else:
            self.version_item = 1
            self.ultima_version_item_id = -1

        super(Item, self).save()
        return Item


# class RelacionItemFaseAnterior (models.Model):
#     id_relacion_fase_anterior = models.AutoField(primary_key=True)
#     id_item_fase_anterior = models.ForeignKey(Item)
#     id_item_fase_actual = models.ForeignKey(Item, related_name='item_relacionados_fase_anterior')
#     relacion_valida = models.BooleanField()
#     # Verdadero: Relacion Valida - Falso: Relacion invalida
#
#
# class RelacionPadreHijo (models.Model):
#     id_relacion_padre_hijo = models.AutoField(primary_key=True)
#     id_item_hijo = models.ForeignKey(Item)
#     id_item_padre = models.ForeignKey(Item, related_name='item_hijos')
#     relacion_valida = models.BooleanField()
#     # Verdadero: Relacion Valida - Falso: Relacion invalida

class Relacion (models.Model):
    del_item = models.ForeignKey(Item, related_name="ItemA")
    al_item = models.ForeignKey(Item, related_name="ItemB")
    tipo = models.CharField(max_length=1)


class ArchivoAdjunto(models.Model):
    id_archivo_adjunto = models.AutoField(primary_key=True)
    filename=models.CharField(max_length=100)
    path_archivo = models.FileField(upload_to='documents/%Y%m%d')
    id_item_relacionado = models.ForeignKey(Item)


class LineaBase(models.Model):
    id_linea_base = models.AutoField(primary_key=True)
    nombre_linea_base = models.CharField(max_length=15)
    creado_por = models.ForeignKey(User)
    fase_linea_base = models.ForeignKey('adm.Fase', verbose_name="Fase")

    def __unicode__(self):
         return self.nombre_linea_base