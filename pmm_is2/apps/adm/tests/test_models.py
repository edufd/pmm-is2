from django.contrib.auth.models import User

__author__ = 'Eduardo'
from django.test import TestCase
from pmm_is2.apps.adm.models import UserProfile
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
      valido = User.objects.filter(username='"aa"').exists()
      if valido==False:
          print "\n---Se ha encontrado el usuario creado"

      print "\n --Buscar un usuario inexistente"
      valido = False
      valido = User.objects.filter(username='"oo"').exists()
      if valido==False:
          print "\n---No existe el usuario buscado"