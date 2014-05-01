from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User, Group, Permission
from django import forms
from pmm_is2.apps.adm.models import UserProfile, Proyecto, Fase
from pmm_is2.apps.des.models import TipoItem


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
                  'costo_monetario', 'estado', 'fecha_inicio', 'fecha_fin', 'plazo', 'lider_de_proyecto')


class FaseForm(forms.ModelForm):
    estado= forms.CharField(widget=forms.HiddenInput(), initial="NOINICIADA")
    id_tipo_item = forms.ModelMultipleChoiceField(
        queryset=TipoItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Fase
        fields = ('nombre_fase',
                  'descripcion','estado','id_tipo_item'
            )



