from django import forms
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


class TipoItemForm(forms.models.ModelForm):

    class Meta:
        model = TipoItem
        fields = ('nombre_tipo_item', 'descripcion')


class AtributoTipoItemForm(forms.models.ModelForm):

    tipo_atributo = forms.CharField(widget=forms.Select(choices=TIPO_ATRIBUTO))
    obligatorio = forms.CharField(widget=forms.Select(choices=OBLIGATORIO))

    class Meta:
        model = Atributo
        fields = {'observacion', 'descripcion', 'obligatorio', 'tipo_atributo', 'nombre_atributo_tipo_item' }


class ArchivoAdjuntoForm(forms.models.ModelForm):
    path_archivo = forms.FileField(label='Selecciona un archivo')
    filename = forms.CharField(max_length=100,label='Nombre Archivo:')
    id_item_relacionado = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)

    class Meta:
       model = ArchivoAdjunto
       fields = ('path_archivo', 'filename', 'id_item_relacionado')


class RelacionesForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(RelacionesForm, self).__init__(*args, **kwargs)

        self.fields['del_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase_id=id_fase, estado='ACTIVO'),
                                                        widget=forms.Select(), required=True)

        self.fields['al_item'] = \
            forms.ModelChoiceField(queryset=Item.objects.filter(id_fase_id=id_fase, estado='ACTIVO'),
                                                        widget=forms.Select(), required=True)

    class Meta:
        model = Relacion
        fields = {'al_item', 'del_item', 'tipo'}


_all_ = [Proyecto, Fase, Item]


class SolicitudForm(forms.ModelForm):
    nombre_proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), widget=forms.Select(), required=False)
    fecha_inicio = forms.DateField(widget=AdminDateWidget)
    nombre_fase = forms.ModelChoiceField(queryset=Fase.objects.filter(estado_fase='FINALIZADA'), widget=forms.Select(), required=False)
    nombre_item = forms.ModelChoiceField(queryset=Item.objects.filter(estado='BLOQUEADO'), widget=forms.Select(), required=False)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=False)
    tipo = forms.ModelMultipleChoiceField(queryset=Tipo.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    descripcion = forms.CharField(label=u"descripcion", widget=forms.Textarea({'cols': 60, 'rows': 10}), error_messages={'required': 'Ingrese observaciones'})
    nombre_linea_base= forms.ModelChoiceField(queryset=LineaBase.objects.filter(estado='CERRADA'), widget=forms.Select(), required=False)
    class Meta:
        model = Solicitud
        fields = ('fecha_inicio', 'nombre_proyecto', 'nombre_fase',
                  'nombre_item', 'usuario', 'estado', 'nombre_linea_base', 'tipo', 'prioridad', 'descripcion')

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget = widgets.AdminDateWidget()
        self.fields['estado'].widget.attrs['readonly'] = True



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
        self.fields['nombre_linea_base'].widget.attrs['readonly'] = True
        self.fields['tipo'].widget.attrs['disabled'] = True
        self.fields['prioridad'].widget.attrs['disabled'] = True
        self.fields['descripcion'].widget.attrs['readonly'] = True