from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from pmm_is2.apps.adm.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'groups')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'groups')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nombre', 'apellido', 'ci', 'telefono')


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'permissions')


class ProjectForm(forms.ModelForm):

    fecha_fin = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'descripcion', 'presupuesto',
                  'fecha_fin', 'lider_proyecto', 'numero_fases')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['fecha_fin'].widget = widgets.AdminDateWidget()


class ProjectMembersForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ('miembros',)


class FaseForm(forms.ModelForm):

    class Meta:
        model = Fase
        fields = ('nombre_fase', 'descripcion', 'tipo_item')


class ComiteForm(forms.ModelForm):
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), widget=forms.Select(), required=False)
    usuario = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Comite
        fields = ('proyecto', 'usuario')



