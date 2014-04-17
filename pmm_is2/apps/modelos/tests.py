from django.test import TestCase

from pmm_is2.apps.modelos.models import Usuario
from pmm_is2.apps.modelos.models import Rol
from pmm_is2.apps.modelos.models import Permiso
from pmm_is2.apps.modelos.models import RolPermiso
from pmm_is2.apps.modelos.models import UsuarioRol

#./manage.py test modelos --desde consola
# Create your tests here.
class UsuarioTestCase (TestCase):
    def setUp (self):
        Usuario.objects.create(nombre="a", apellido="b",ci="4696038",username="aa",telefono="0971113859",contrasenha="adrisila")
        #Usuario.objects.create(nombre="a", apellido="b",ci="4696038",username="aa",telefono="0971113859",contrasenha="adrisila")
    def test_traer(self):
        self.assertTrue(Usuario.objects.get(username="aa"))

class RolTestCase (TestCase):
    def setUp (self):
        Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
    def test_Roltraer(self):
        self.assertTrue(Rol.objects.get(nombre="Administrador"))#nombre uno solo retornar

class PermisoTestCase (TestCase):
    def setUp (self):
        Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
    def test_Permisotraer(self):
        self.assertTrue(Permiso.objects.get(nombre="AgregarUser"))#nombre uno solo retornar

class RoPermisoTestCase(TestCase):
    def setUp (self):
        Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
        uno=Rol.objects.get(nombre="Administrador")
        Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
        dos=Permiso.objects.get(nombre="AgregarUser")
        e=RolPermiso(id_rol=uno, id_permiso=dos)
        e.save()
    def test_RolPermisotraer(self):
        self.assertTrue(RolPermiso.objects.get(pk=1))

class UsuarioRolTestCase(TestCase):
    def setUp (self):
        Rol.objects.create(nombre="Lider", descripcion="accesoParcial")
        traer1=Rol.objects.get(nombre="Lider")
        Permiso.objects.create(nombre="ModificarUser", descripcion="ModificaUsuarios", tipo=2)
        traer2=Permiso.objects.get(nombre="ModificarUser")
        e=RolPermiso(id_rol=traer1, id_permiso=traer2)
        e.save()
        Usuario.objects.create(nombre="b", apellido="b",ci="4696039",username="mm",telefono="0971113859",contrasenha="adrisila")
        traer3=Usuario.objects.get(nombre="b")
        f=UsuarioRol(id_rol=traer1, id_usuario=traer3)
        f.save()
    def test_UsuarioRoltraer(self):
        self.assertTrue(UsuarioRol.objects.get(pk=1))

