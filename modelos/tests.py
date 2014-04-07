from django.test import TestCase
from modelos.models import Usuario
from modelos.models import Rol
from modelos.models import Permiso
from modelos.models import RolPermiso
#from modelos.models import UsuarioRol
#./manage.py test modelos --desde consola
# Create your tests here.
class UsuarioTestCase (TestCase):
    def setUp (self):
        Usuario.objects.create(nombre="a", apellido="b",ci="4696038",username="aa",telefono="0971113859",contrasenha="adrisila")
        #Usuario.objects.create(nombre="a", apellido="b",ci="4696038",username="aa",telefono="0971113859",contrasenha="adrisila")
    def test_traer(self):
        self.assertTrue(Usuario.objects.get(username="aa"))#username y ci tambien primary-key uno solo retornar

class RolTestCase (TestCase):
    def setUp (self):
        Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
    def test_Roltraer(self):
        self.assertTrue(Rol.objects.get(nombre="Administrador"))#nombre tambien primary-key uno solo retornar

class PermisoTestCase (TestCase):
    def setUp (self):
        Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
    def test_Permisotraer(self):
        self.assertTrue(Permiso.objects.get(nombre="AgregarUser"))#nombre tambien primary-key uno solo retornar

class RoPermisoTestCase(TestCase):
    def setUp (self):
        Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
        uno=Rol.objects.get(id_rol=1)
        Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
        dos=Permiso.objects.get(id_permiso=2)
        e=RolPermiso(id_rol=uno, id_permiso=dos)
        e.save()
    def test_RolPermisotraer(self):
        self.assertTrue(RolPermiso.objects.get(pk=1))

