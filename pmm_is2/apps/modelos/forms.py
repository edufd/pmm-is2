from AptUrl.Helpers import _
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from pmm_is2.apps.modelos.models import Usuario, Rol


class UserForm(forms.ModelForm):
    contrasenha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('id_usuario','username', 'nombre', 'apellido', 'ci', 'telefono', 'contrasenha')


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ('id_rol','nombre','descripcion')


class RolForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(queryset=Rol.objects.all(),
                                          label=_('Select tags'),
                                          required=False,
                                          widget=FilteredSelectMultiple(
                                                    _('tags'),
                                                    False,
                                                 ))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']
