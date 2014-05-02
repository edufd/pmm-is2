from django import forms
from pmm_is2.apps.des.models import TipoItem

class TipoItemForm(forms.models.ModelForm):

    class Meta:
        model = TipoItem
        fields = ('nombre_tipo_item', 'descripcion')


