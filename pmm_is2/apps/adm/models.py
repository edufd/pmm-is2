from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Max
from django.utils.datetime_safe import datetime
from pmm_is2.apps.des.models import TipoItem
# Create your models here.

FASES_ESTADOS = (
    ('ABIERTA', 'ABIERTA'),
    ('FINALIZADA', 'FINALIZADA'),
    ('NO-INICIADA', 'NO-INICIADA'),
)

PROYECTOS_ESTADOS = (
    ('NO-INICIADO', 'NO-INICIADO'),
    ('INICIADO', 'INICIADO'),
    ('FINALIZADO', 'FINALIZADO'),
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
    costo_temporal = models.IntegerField(default=0)
    costo_monetario = models.IntegerField(default=0)
    estado_proyecto = models.CharField(max_length=11, choices=PROYECTOS_ESTADOS, default='NO-INICIADO')
    #cambiar despues para que sea la fecha actual al crear
    fecha_inicio = models.DateField(blank=True, default=datetime.now())
    fecha_fin = models.DateField()
    plazo = models.IntegerField()
    lider_proyecto = models.ForeignKey(User)
    #para el perfil de proyecto es interesante

    def __unicode__(self):
        return self.nombre_proyecto

    class Meta:
        #db_table = 'proyecto'
        app_label = 'adm'


class UsuarioProyecto(models.Model):
    id_usuario_proyecto = models.AutoField(primary_key=True)
    #roles
    roles_proyecto = models.ForeignKey(Group)
    proyectos = models.ForeignKey(Proyecto, related_name='usuario_proyecto')
    usuario_proyecto = models.ForeignKey(User)


class Fase(models.Model):
    id_fase = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto)
    nombre_fase = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    estado_fase = models.CharField(max_length=10, choices=FASES_ESTADOS, default='ABIERTA')
    numero_secuencia = models.IntegerField(blank=True)
    id_tipo_item = models.ManyToManyField(TipoItem)

    class Meta:
        #db_table = 'fase'
        app_label = 'adm'


    #Para aumentar el numero por cada fase creada
    def save(self):
        primera_fase = False
        primera_fase = Fase.objects.filter(numero_secuencia=1, proyecto_id=self.proyecto_id).exists()
        if (primera_fase is True):
            maximo = Fase.objects.filter(proyecto_id=self.proyecto_id).aggregate(Max('numero_secuencia'))['numero_secuencia__max']
            numero_secuencia = Fase.objects.get(proyecto_id=self.proyecto_id, numero_secuencia=maximo)
            top = numero_secuencia.numero_secuencia + 1
            self.numero_secuencia = top
        else:
            self.numero_secuencia = 1

        super(Fase, self).save()
        return Fase




