__author__ = 'VICTOR'

from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminDateWidget
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.forms.extras import SelectDateWidget
from pmm_is2.apps.gdc.models import Tipo, Solicitud, LineaBase
from pmm_is2.apps.adm.models import Proyecto,Fase
from pmm_is2.apps.des.models import Item
from pmm_is2.apps.gdc.models import PRIORIDAD_CHOICES
from pmm_is2.apps.gdc.models import opciones
_all_=[Proyecto,Fase,Item]


class SolicitudForm(forms.ModelForm):
    nombre_proyecto= forms.ModelChoiceField(queryset=Proyecto.objects.all(), widget=forms.Select(), required=False)
    fecha_inicio = forms.DateField(widget=AdminDateWidget)
    nombre_fase= forms.ModelChoiceField(queryset=Fase.objects.all(), widget=forms.Select(), required=False)
    nombre_item= forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)
    usuario= forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=False)
    tipo = forms.ModelMultipleChoiceField(queryset=Tipo.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    descripcion= forms.CharField(label=u"descripcion", widget=forms.Textarea({'cols': 80, 'rows': 20}), error_messages={'required': 'Ingrese observaciones'})

    class Meta:
        model = Solicitud
        fields = ('fecha_inicio', 'nombre_proyecto', 'nombre_fase', 'nombre_item','usuario','estado','nombre_linea_base','tipo','prioridad','descripcion')
    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget = widgets.AdminDateWidget()
        self.fields['estado'].widget.attrs['readonly'] = True
        self.fields['nombre_linea_base'].widget.attrs['readonly'] = True


class SolicitudRecibidoForm(forms.ModelForm):
    nombre_proyecto= forms.ModelChoiceField(queryset=Proyecto.objects.all(), widget=forms.Select(), required=False)
    fecha_inicio = forms.DateField(widget=AdminDateWidget)
    nombre_fase= forms.ModelChoiceField(queryset=Fase.objects.all(), widget=forms.Select(), required=False)
    nombre_item= forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)
    usuario= forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=False)
    tipo = forms.ModelMultipleChoiceField(queryset=Tipo.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    descripcion= forms.CharField(label=u"descripcion", widget=forms.Textarea({'cols': 80, 'rows': 20}), error_messages={'required': 'Ingrese observaciones'})
    opciones= forms.ModelChoiceField(queryset=opciones.objects.all(), widget = forms.RadioSelect, required=False)
    comentarios= forms.CharField(label=u"comentarios", widget=forms.Textarea({'cols': 80, 'rows': 20}), error_messages={'required': 'Ingrese comentarios'})

    class Meta:
        model = Solicitud
        fields = ('fecha_inicio', 'nombre_proyecto', 'nombre_fase', 'nombre_item',
                  'usuario','estado','nombre_linea_base','tipo',
                  'prioridad','descripcion','opciones','comentarios')
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


class LineaBaseForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        #self.fields['items'] = forms.MultipleChoiceField(queryset=Item.objects.select_related('fase').filter(id_fase=id_fase),
        #                                                 widget=forms.Select(), required=False)

    class Meta:
        model = LineaBase
        fields = ('nombre_linea_base', 'estado', 'tipo', 'numero', 'creado_por', 'items')