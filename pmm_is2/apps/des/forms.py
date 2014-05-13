from django import forms
from pmm_is2.apps.des.models import TipoItem

from pmm_is2.apps.des.models import ArchivoAdjunto
from pmm_is2.apps.des.models import Item

#para probar archivo adjunto luego eliminar y poner como se debe
class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('nombre_item', 'version_item','prioridad','complejidad','ultima_version_item_id')


class TipoItemForm(forms.models.ModelForm):

    class Meta:
        model = TipoItem
        fields = ('nombre_tipo_item', 'descripcion')


class ArchivoAdjuntoForm(forms.Form):
    id_archivo_adjunto = forms.IntegerField(widget=forms.HiddenInput,required=False)
    path_archivo = forms.CharField(widget=forms.FileInput,max_length=300,error_messages={'required': 'Seleccione el archivo adjunto'},)
    path_archivo_editable = forms.CharField(max_length=300,required=False)
    item_archivo_adjunto = forms.CharField(label=u"Item Archivo Adjunto",error_messages={'required': 'Ingrese Item Archivo Adjunto'})
    editar_archivo_adjunto = False
    id_archivo_adjunto_valor = -1

    def __init__(self, *args, **kwargs):
         super(ArchivoAdjuntoForm, self).__init__(*args, **kwargs)
         self.fields['path_archivo_editable'].widget.attrs['readonly'] = True
         self.fields['item_archivo_adjunto'].widget.attrs['readonly'] = True

    def clean(self):
        return self.cleaned_data

    def clean_id_archivo_adjunto(self):
        if self.cleaned_data.get('id_archivo_adjunto') != -1:
            self.editar_archivo_adjunto = True
            self.id_archivo_adjunto_valor = self.cleaned_data.get('id_archivo_adjunto')


