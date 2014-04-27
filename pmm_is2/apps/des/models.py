from django.db import models

class Atributo(models.Model):
    id_atributo = models.AutoField(primary_key=True)
    nombre_atributo_tipo_item = models.CharField(max_length=200,unique=True )
    tipo_atributo = models.CharField(max_length=1)#N:NUMERICO #T:TEXTO
    obligatorio=models.CharField(max_length=1)#Y:OBLIGATORIO #N;NO ES OBLIGATORIO
    descripcion = models.CharField(max_length=200)
    observacion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'Atributo'

class TipoItem(models.Model):
    id_tipo_item = models.AutoField(primary_key=True)
    nombre_tipo_item = models.CharField(max_length=200,unique=True )
    descripcion = models.CharField(max_length=200)
    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'TipoItem'

class AtributoTipoItem(models.Model):
    id_atributo_tipo_item = models.AutoField(primary_key=True)
    id_tipo_item = models.ForeignKey('TipoItem')
    id_atributo = models.ForeignKey('Atributo')
    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'AtributoTipoItem'
        unique_together = (("id_tipo_item", " id_atributo"),)

class TipoItemProyecto(models.Model):
    id_tipo_item_proyecto = models.AutoField(primary_key=True)
    nombre_tipo_item_proyecto = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    id_tipo_item = models.ForeignKey('TipoItem')
    id_proyecto = models.ForeignKey('Proyecto')

    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'TipoItem_proyecto'
        unique_together = (("id_tipo_item", " id_proyecto"),)

class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre_item = models.CharField(unique=False,max_length=200)
    version_item = models.IntegerField()
    prioridad = models.IntegerField()## Deberá tener del 1 al  10
    estado = models.CharField(max_length=1)# I:Inactivo  B:Bloqueado C:Revisión A:Aprobado D:Desaprobado
    descripcion = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=5000)
    complejidad = models.IntegerField()
    ultima_version_item_id = models.IntegerField()
    id_tipo_item = models.ForeignKey(TipoItemProyecto,related_name='Item')
    fase_item = models.ForeignKey(Fase, related_name='tipo_fase')

    def obtener_historial_item(self):
        "lista de items que pertenecen al historial del item"
        return 'Redefinir para que retorne el historial'
        historial = property(obtener_historial_item)

