from django import forms
from django.db.models import Q
from pmm_is2.apps.des.models import *
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminDateWidget
from django.contrib.auth.models import User, Group, Permission
from django.forms.extras import SelectDateWidget
from pmm_is2.apps.adm.models import Proyecto, Fase
from pmm_is2.apps.des.models import Solicitud
from pmm_is2.apps.gdc.models import LineaBase


#para probar archivo adjunto luego eliminar y poner como se debe
class ItemForm(forms.models.ModelForm):
    complejidad = forms.IntegerField(label=u"Complejidad (del 1 al 10)", error_messages={'required': 'Ingrese la complejidad del item'}, max_value=10)
    descripcion = forms.CharField(label=u"Descripcion", max_length=30, error_messages={'required': 'Ingrese una descripcion del item'})
    observaciones = forms.CharField(label=u"Observaciones", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese observaciones'})

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(ItemForm, self).__init__(*args, **kwargs)

        self.fields['id_tipo_item'] = \
            forms.ModelChoiceField(queryset=TipoItem.objects.select_related('fase').filter(fase=id_fase),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Item
        fields = ('nombre_item', 'prioridad', 'complejidad', 'costo', 'observaciones', 'id_tipo_item',
                  'descripcion')


class ItemFormEdit(forms.models.ModelForm):
    complejidad = forms.IntegerField(label=u"Complejidad (del 1 al 10)", error_messages={'required': 'Ingrese la complejidad del item'}, max_value=10)
    descripcion = forms.CharField(label=u"Descripcion", max_length=30, error_messages={'required': 'Ingrese una descripcion del item'})
    observaciones = forms.CharField(label=u"Observaciones", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese observaciones'})

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(ItemFormEdit, self).__init__(*args, **kwargs)

        self.fields['id_tipo_item'] = \
            forms.ModelChoiceField(queryset=TipoItem.objects.select_related('fase').filter(fase=id_fase),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Item
        fields = ('nombre_item', 'prioridad', 'estado', 'complejidad', 'costo', 'observaciones', 'id_tipo_item',
                  'descripcion')


class TipoItemForm(forms.models.ModelForm):
    atributo = forms.ModelChoiceField(queryset=Atributo.objects.all().order_by('nombre_atributo_tipo_item'), required=False)

    class Meta:
        model = TipoItem
        fields = ('nombre_tipo_item', 'descripcion', 'atributo')


class AtributoTipoItemForm(forms.models.ModelForm):

    tipo_atributo = forms.CharField(widget=forms.Select(choices=TIPO_ATRIBUTO))
    obligatorio = forms.CharField(widget=forms.Select(choices=OBLIGATORIO))

    class Meta:
        model = Atributo
        fields = {'observacion', 'detalle', 'obligatorio', 'tipo_atributo', 'nombre_atributo_tipo_item'}


class ArchivoAdjuntoForm(forms.models.ModelForm):
    path_archivo = forms.FileField(label='Selecciona un archivo')
    filename = forms.CharField(max_length=100, label='Nombre Archivo:')
    id_item_relacionado = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)

    class Meta:
       model = ArchivoAdjunto
       fields = ('filename', 'id_item_relacionado', 'path_archivo')


class RelacionesForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(RelacionesForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'del_item',
            'tipo',
            'al_item'
        ]

        self.fields['del_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase=id_fase).filter(Q(estado='REVISION') | Q(estado='BLOQUEADO' ) | Q(estado='APROBADO')).order_by('id_item'),
                                                        widget=forms.Select(), required=True)

        fase = Fase.objects.get(pk=id_fase)
        proyecto_id = fase.proyecto_id
        proyecto = Proyecto.objects.get(pk=proyecto_id)
        fases = proyecto.fases.all()

        self.fields['al_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase__in=fases).order_by('id_item'),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Relacion
        fields = {'del_item', 'al_item', 'tipo'}


class RelationFixForm(forms.models.ModelForm):

    tipo = forms.CharField(widget=forms.Select(choices=RELACION_TIPO), initial='ANTECESOR-SUCESOR')

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        id_item = kwargs.pop('item_id')

        super(RelationFixForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'del_item',
            'tipo',
            'al_item'
        ]

        self.fields['del_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase_id=id_fase).exclude(id_item=id_item).order_by('id_item'),
                                                        widget=forms.Select(), required=True)

        fase = Fase.objects.get(pk=id_fase)
        fase_siguiente = fase.numero_secuencia + 1
        fase_siguiente = Fase.objects.get(proyecto_id=fase.proyecto_id, numero_secuencia=fase_siguiente)


        self.fields['al_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase=fase_siguiente).order_by('id_item'),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Relacion
        fields = {'del_item', 'al_item', 'tipo'}


class RelationFixReviveForm(forms.models.ModelForm):

    tipo = forms.CharField(widget=forms.Select(choices=RELACION_TIPO), initial='ANTECESOR-SUCESOR')

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        id_item = kwargs.pop('item_id')
        item_id_sucesor = kwargs.pop('item_id_sucesor')

        super(RelationFixReviveForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'del_item',
            'tipo',
            'al_item'
        ]

        self.fields['del_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_item=id_item),
                                                        widget=forms.Select(), required=True)

        fase = Fase.objects.get(pk=id_fase)
        fase_siguiente = fase.numero_secuencia + 1
        fase_siguiente = Fase.objects.get(proyecto_id=fase.proyecto_id, numero_secuencia=fase_siguiente)

        self.fields['al_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase=fase_siguiente).exclude(id_item=item_id_sucesor),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Relacion
        fields = {'del_item', 'al_item', 'tipo'}


_all_ = [Proyecto, Fase, Item]


class SolicitudForm(forms.ModelForm):
    #nombre_proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.none(), widget=forms.Textarea({'cols': 50, 'rows': 2}), required=True)
    fecha_inicio = forms.DateField(widget=AdminDateWidget)
    #nombre_fase = forms.ModelChoiceField(queryset=Fase.objects.filter(estado_fase='CERRADA'), widget=forms.Select(), required=True)
    nombre_item = forms.ModelChoiceField(queryset=Item.objects.filter(estado='BLOQUEADO'), widget=forms.Select(), required=True)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=True)
    tipo = forms.ModelMultipleChoiceField(queryset=Tipo.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    descripcion = forms.CharField(label=u"descripcion", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese observaciones'})
    nombre_linea_base = forms.ModelChoiceField(queryset=LineaBase.objects.filter(estado='CERRADA'), widget=forms.Select(), required=True)

    class Meta:
        model = Solicitud
        fields = ('fecha_inicio', 'nombre_item', 'usuario', 'estado', 'nombre_linea_base', 'tipo', 'prioridad', 'descripcion')

    def __init__(self,idfase, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget = widgets.AdminDateWidget()
        self.fields['estado'].widget.attrs['readonly'] = True
        #self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(id_proyecto=idproyecto)
        #self.fields['nombre_fase'].queryset = Fase.objects.filter(id_fase=idfase, estado_fase='CERRADA')

        self.fields['nombre_item'].queryset = Item.objects.filter(id_fase=idfase, estado='BLOQUEADO')
        self.fields['nombre_linea_base'].queryset = LineaBase.objects.filter(fase=idfase, estado='CERRADA')


class SolicitudRecibidoForm(forms.ModelForm):
    nombre_proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), widget=forms.Select(), required=False)
    fecha_inicio = forms.DateField(widget=AdminDateWidget)
    nombre_fase = forms.ModelChoiceField(queryset=Fase.objects.all(), widget=forms.Select(), required=False)
    nombre_item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=False)
    tipo = forms.ModelMultipleChoiceField(queryset=Tipo.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    descripcion = forms.CharField(label=u"descripcion", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese observaciones'})
    opciones = forms.ModelChoiceField(queryset=opciones.objects.all(), widget=forms.RadioSelect, required=False)
    comentarios = forms.CharField(label=u"comentarios", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese comentarios'})

    class Meta:
        model = Solicitud
        fields = ('fecha_inicio', 'nombre_proyecto', 'nombre_fase', 'nombre_item',
                  'usuario', 'estado','nombre_linea_base', 'tipo',
                  'prioridad', 'descripcion', 'opciones', 'comentarios')

    def __init__(self, *args, **kwargs):
        super(SolicitudRecibidoForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget.attrs['readonly'] = True
        self.fields['nombre_proyecto'].widget.attrs['disabled'] = True
        self.fields['nombre_fase'].widget.attrs['disabled'] = True
        self.fields['nombre_item'].widget.attrs['disabled'] = True
        self.fields['usuario'].widget.attrs['disabled '] = True
        self.fields['estado'].widget.attrs['readonly'] = True
        self.fields['nombre_linea_base'].widget.attrs['disabled'] = True
        self.fields['tipo'].widget.attrs['disabled'] = True
        self.fields['prioridad'].widget.attrs['disabled'] = True
        self.fields['descripcion'].widget.attrs['readonly'] = True