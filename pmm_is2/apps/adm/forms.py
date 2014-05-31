from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User, Group
from django import forms
from pmm_is2.apps.adm.models import UserProfile, Proyecto, Fase, Comite


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
    fecha_fin = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'descripcion', 'presupuesto', 'costo_temporal',
                  'costo_monetario', 'fecha_fin', 'plazo', 'lider_proyecto', 'numero_fases')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['fecha_fin'].widget = widgets.AdminDateWidget()


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



