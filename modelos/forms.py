from modelos.models import Usuario
from django import forms

class UserForm(forms.ModelForm):
    contrasenha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('id_usuario','username', 'nombre', 'apellido', 'ci', 'telefono', 'contrasenha')

