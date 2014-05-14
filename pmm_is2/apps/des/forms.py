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


class ArchivoAdjuntoForm(forms.models.ModelForm):
    path_archivo = forms.FileField(label='Selecciona un archivo')
    filename = forms.CharField(max_length=100,label='Nombre Archivo:')
    id_item_relacionado = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(), required=False)
    class  Meta:
       model = ArchivoAdjunto
       fields = ('path_archivo','filename','id_item_relacionado')





