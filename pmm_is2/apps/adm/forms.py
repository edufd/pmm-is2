from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User, Group, Permission
from django import forms
from pmm_is2.apps.adm.models import UserProfile, Proyecto, Fase


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'groups')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nombre', 'apellido', 'ci', 'telefono')


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'permissions')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'descripcion', 'presupuesto', 'costo_temporal',
                  'costo_monetario', 'estado', 'fecha_inicio', 'fecha_fin', 'plazo', 'lider_proyecto')


#nombre_fase = models.CharField(max_length=200)
    # descripcion = models.CharField(max_length=200)
    # estado = models.CharField(max_length=10, choices=FASES_ESTADOS)
    # numero_secuencia = models.IntegerField(blank=True, null=True)
class FaseForm(forms.ModelForm):
    class Meta:
        model = Fase
        fields = ('nombre_fase', 'descripcion', 'estado', 'numero_secuencia')