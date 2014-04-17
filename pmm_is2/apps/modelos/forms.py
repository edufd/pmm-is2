from django import forms

from pmm_is2.apps.modelos.models import Usuario
from pmm_is2.apps.modelos.models import Rol


class UserForm(forms.ModelForm):
    contrasenha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('id_usuario','username', 'nombre', 'apellido', 'ci', 'telefono', 'contrasenha')



class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ('id_rol','nombre','descripcion')


