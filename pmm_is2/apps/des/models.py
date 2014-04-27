from django.db import models

class TipoItem(models.Model):
    id_tipo_item = models.AutoField(primary_key=True)
    nombre_tipo_item = models.CharField(max_length=200,unique=True )
    descripcion = models.CharField(max_length=200)

    def __unicode__(self):
        return self.descripcion
    class Meta:
        db_table = 'TipoItem'

