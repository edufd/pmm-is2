from django.contrib.auth.models import User, Group

__author__ = 'Eduardo'
from django.test import TestCase
from pmm_is2.apps.adm.models import UserProfile, Proyecto, Fase
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):

    def test_default_nombre(self):
        user = UserProfile()
        self.assertEqual(user.nombre, '')

    def test_default_apellido(self):
        user = UserProfile()
        self.assertEqual(user.apellido, '')

    def test_duplicate_user_are_invalid(self):
        user_ = User.objects.create(username="Eduardo", password="edu")
        UserProfile.objects.create(user=user_, ci=3523157, telefono=605390)
        with self.assertRaises(ValidationError):
            user = UserProfile(user=user_, ci=3523157, telefono=605390)
            user.full_clean()

class UsuarioTestCase (TestCase):

  def setUp (self):
     print "\n TEST USUARIO"
     print "\n --Buscar el usuario creado"
     User.objects.create(username="aa", password="aa")

  def test_traer(self):
      valido = False
      valido = User.objects.filter(username="aa").exists()
      if valido==True:
          print "\n---Se ha encontrado el usuario creado"

      print "\n --Buscar un usuario inexistente"
      valido = True
      valido = User.objects.filter(username='"oo"').exists()
      if valido==False:
          print "\n---No existe el usuario buscado"

class GrupoTestCase (TestCase):

  def setUp (self):
     print "\n TEST GRUPO"
     print "\n --Buscar el Grupo creado"
     Group.objects.create(name="aa")

  def test_traer(self):
      valido = False
      valido = Group.objects.filter(name="aa").exists()
      if valido==True:
          print "\n---Se ha encontrado el Grupo creado"

      print "\n --Buscar un Grupo inexistente"
      valido = True
      valido = Group.objects.filter(name='"oo"').exists()
      if valido==False:
          print "\n---No existe el grupo buscado"


class ProyectoTestCase (TestCase):

  def setUp (self):
     print "\n TEST PROYECTO"
     print "\n --Buscar el PROYECTO creado"
     Proyecto.objects.create(nombre_proyecto='Tv Chat', descripcion='Analisis de Requerimientos',
                                           presupuesto=3000000, estado_proyecto='NO-INICIADO',
                                           numero_fases=2, fecha_inicio='2014-05-11', fecha_fin='2014-05-31',
                                           plazo=21, lider_proyecto=User.objects.create(username="aa", password="aa"))

  def test_traer(self):
      valido = False
      valido = Proyecto.objects.filter(nombre_proyecto='Tv Chat').exists()
      if valido==True:
          print "\n---Se ha encontrado el PROYECTO creado"

      print "\n --Buscar un PROYECTO inexistente"
      valido = True
      valido = Proyecto.objects.filter(nombre_proyecto='Tv Chat2').exists()
      if valido==False:
          print "\n---No existe el PROYECTO buscado"

# class FaseTestCase (TestCase):
#
#   def setUp (self):
#      print "\n TEST FASE"
#      print "\n --Buscar la FASE creada"
#      proyecto = Proyecto.objects.create(nombre_proyecto='Tv Chat', descripcion='Analisis de Requerimientos',
#                                            presupuesto=3000000, estado_proyecto='NO-INICIADO',
#                                            numero_fases=2, fecha_inicio='2014-05-11', fecha_fin='2014-05-31',
#                                            plazo=21, lider_proyecto=User.objects.create(username="aa", password="aa"))
#      Fase.objects.create(proyecto=proyecto, nombre_fase='Analisis',
#                                    descripcion='Analisis de Requerimientos', estado_fase='ABIERTA',
#                                    numero_secuencia=1)
#
#   def test_traer(self):
#       valido = False
#       valido = Fase.objects.filter(nombre_fase='Analisis').exists()
#       if valido==True:
#           print "\n---Se ha encontrado la FASE creada"
#
#       print "\n --Buscar una FASE inexistente"
#       valido = True
#       valido = Fase.objects.filter(nombre_fase='Tv Chat2').exists()
#       if valido==False:
#           print "\n---No existe la FASE buscada"