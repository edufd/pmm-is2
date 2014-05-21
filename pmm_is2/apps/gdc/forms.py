from django import forms
from pmm_is2.apps.des.models import Item
from pmm_is2.apps.gdc.models import LineaBase


class LineaBaseForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        self.fields["items"].queryset = Item.objects.filter(id_fase_id=id_fase)

    class Meta:
        model = LineaBase
        fields = ('nombre_linea_base', 'tipo', 'numero', 'creado_por', 'items')


class LineaBaseFormEdit(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(LineaBaseFormEdit, self).__init__(*args, **kwargs)
        #self.fields["items"] = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = LineaBase
        fields = ('nombre_linea_base', 'estado', 'tipo', 'numero', 'creado_por', 'items')