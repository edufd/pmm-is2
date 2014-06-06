from django.db import models
from django.contrib.auth.models import User

from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.des.models import Item






LINEA_BASE_ESTADOS = (
    ('ABIERTA', 'ABIERTA'),
    ('REVISION', 'REVISION'),
    ('CERRADA', 'CERRADA'),
)

#Cargar con Parcial Total
class opcionesLineaBase(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    opcion1 = models.CharField(max_length=15)

    def __unicode__(self):
        return self.opcion1

class LineaBase(models.Model):
    id_linea_base = models.AutoField(primary_key=True)
    nombre_linea_base = models.CharField(max_length=30)
    estado = models.CharField(max_length=10, choices=LINEA_BASE_ESTADOS, default='ABIERTA')
    opciones = models.ForeignKey(opcionesLineaBase, null=True)
    creado_por = models.ForeignKey(User)
    fase = models.ForeignKey(Fase, verbose_name="Fase")
    items = models.ManyToManyField(Item)

    def __unicode__(self):
        return self.nombre_linea_base

    class Meta:
        #db_table = 'LineaBase'
        app_label = 'gdc'

