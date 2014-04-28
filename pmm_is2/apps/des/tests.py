from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User, Group
#from pmm_is2.apps.des.models import Item
from pmm_is2.apps.des.models import Atributo
#from pmm_is2.apps.des.models import TipoItem
#from pmm_is2.apps.des.models import AtributoTipoItem
#from pmm_is2.apps.des.models import TipoItemProyecto


#./manage.py test modelos --desde consola
# Create your tests here.

class AtributoTestCase (TestCase):
   def setUp (self):
       print "\n TEST ATRIBUTO"
       print "\n --Buscar el atributo creado"
       Atributo.objects.create(nombre_atributo_tipo_item="detalles", tipo_atributo="b",obligatorio="Y",descripcion="aa",observacion="CC")
   def test_Atributotraer(self):
       valido = False
       valido = Atributo.objects.filter(nombre_atributo_tipo_item='"detalles"').exists()
       if valido==False:
           print "\n---Se ha encontrado el atributo creado"

       print "\n --Buscar un atributo inexistente"
       valido = False
       valido = User.objects.filter(nombre_atributo_tipo_item='"detallesExtras"').exists()
       if valido==False:
           print "\n---No existe el atributo buscado"

# class RolTestCase (TestCase):
#   def setUp (self):
#       Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
#   def test_Roltraer(self):
#       self.assertTrue(Rol.objects.get(nombre="Administrador"))#nombre uno solo retornar

# class PermisoTestCase (TestCase):
#    def setUp (self):
#       Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
#   def test_Permisotraer(self):
#       self.assertTrue(Permiso.objects.get(nombre="AgregarUser"))#nombre uno solo retornar

# class RoPermisoTestCase(TestCase):
#     def setUp (self):
#        Rol.objects.create(nombre="Administrador", descripcion="accesoTotal")
#        uno=Rol.objects.get(nombre="Administrador")
#        Permiso.objects.create(nombre="AgregarUser", descripcion="AgregaUsuarios", tipo=1)
#        dos=Permiso.objects.get(nombre="AgregarUser")
#        e=RolPermiso(id_rol=uno, id_permiso=dos)
#        e.save()
#    def test_RolPermisotraer(self):
#        self.assertTrue(RolPermiso.objects.get(pk=1))

# class UsuarioRolTestCase(TestCase):
#    def setUp (self):
#        Rol.objects.create(nombre="Lider", descripcion="accesoParcial")
#        traer1=Rol.objects.get(nombre="Lider")
#        Permiso.objects.create(nombre="ModificarUser", descripcion="ModificaUsuarios", tipo=2)
#        traer2=Permiso.objects.get(nombre="ModificarUser")
#        e=RolPermiso(id_rol=traer1, id_permiso=traer2)
#        e.save()
#        Usuario.objects.create(nombre="b", apellido="b",ci="4696039",username="mm",telefono="0971113859",contrasenha="adrisila")
#        traer3=Usuario.objects.get(nombre="b")
#        f=UsuarioRol(id_rol=traer1, id_usuario=traer3)
#        f.save()
#    def test_UsuarioRoltraer(self):
#        self.assertTrue(UsuarioRol.objects.get(pk=1))

