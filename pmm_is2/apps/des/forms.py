from django import forms

from pmm_is2.apps.des.models import ArchivoAdjunto, TipoItem, Atributo
from pmm_is2.apps.des.models import Item, ESTADO_CHOICES, PRIORIDAD_CHOICES, TIPO_ATRIBUTO, OBLIGATORIO


#para probar archivo adjunto luego eliminar y poner como se debe
class ItemForm(forms.models.ModelForm):
    prioridad = forms.CharField(max_length=4, widget=forms.Select(choices=PRIORIDAD_CHOICES))
    estado = forms.CharField(max_length=3, widget=forms.Select(choices=ESTADO_CHOICES))
    complejidad = forms.IntegerField(label=u"Complejidad (del 1 al 10)", error_messages={'required': 'Ingrese la complejidad del item'}, max_value=10)
    descripcion = forms.CharField(label=u"Descripcion", max_length=30, error_messages={'required': 'Ingrese una descripcion del item'})
    observaciones = forms.CharField(label=u"Observaciones", widget=forms.Textarea({'cols': 80, 'rows': 20}), error_messages={'required': 'Ingrese observaciones'})

    # def __init__(self, *args, **kwargs):
    #     tipo_item = kwargs.pop('tipo_item')
    #     super(ItemForm, self).__init__(*args, **kwargs)
    #     self.fields['id_tipo_item'] = forms.ModelChoiceField(queryset=TipoItem.objects.filter(id_tipo_item=tipo_item), widget=forms.Select(), required=False)

    class Meta:
        model = Item
        fields = ('nombre_item', 'prioridad', 'estado', 'complejidad', 'observaciones', 'id_tipo_item', 'descripcion')


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
    class  Meta:
       model = ArchivoAdjunto
       fields = ('path_archivo','filename','id_item_relacionado')





