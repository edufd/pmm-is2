from django.db import models

class TipoItem(models.Model):
    id_tipo_item = models.AutoField(primary_key=True)
    nombre_tipo_item = models.CharField(max_length=200,unique=True )
    descripcion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'TipoItem'

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
