from django import forms
from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.des.models import Item
from pmm_is2.apps.gdc.models import LineaBase


class LineaBaseForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        #self.fields['items'] = forms.MultipleChoiceField(queryset=Item.objects.select_related('fase').filter(id_fase=id_fase),
        #                                                 widget=forms.Select(), required=False)

    class Meta:
        model = LineaBase
        fields = ('nombre_linea_base', 'estado', 'tipo', 'numero', 'creado_por', 'items')

