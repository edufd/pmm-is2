from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User, Group
from pmm_is2.apps.des.models import Atributo
from pmm_is2.apps.des.models import TipoItem
#from pmm_is2.apps.des.models import AtributoTipoItem
#from pmm_is2.apps.des.models import TipoItemProyecto


#./manage.py test modelos --desde consola
# Create your tests here.

class AtributoTestCase (TestCase):
   def setUp (self):
       print "\n TEST ATRIBUTO"
       print "\n --Buscar el atributo creado"
       Atributo.objects.create(nombre_atributo_tipo_item="detalles", tipo_atributo="b",obligatorio="Y",descripcion="aa",observacion="CC")
   def test_traer(self):
             self.assertTrue(Atributo.objects.get(nombre_atributo_tipo_item="detalles"))
   def test_Atributotraer(self):
       valido = False
       valido = Atributo.objects.filter(nombre_atributo_tipo_item="detalles").exists()

       if valido:
           print "\n---Se ha encontrado el atributo creado"
       if valido==False:
           print "\n---No se ha creado el atributo"
       print "\n --Buscar un atributo inexistente"
       valido = False
       valido = Atributo.objects.filter(nombre_atributo_tipo_item="detallesExtras").exists()
       if valido==False:
           print "\n---No existe el atributo buscado"


class TipoItemTestCase (TestCase):
    def setUp (self):
        print "\n TEST TIPOITEM"
        print "\n --Buscar el TipoItem creado"
        TipoItem.objects.create(nombre_tipo_item="detalles", descripcion="aa")
    def test_TipoItemtraer(self):
        valido = False
        valido = TipoItem.objects.filter(nombre_tipo_item="detalles").exists()
        if valido:
            print "\n---Se ha encontrado el TipoItem creado"
        if valido==False:
            print "\n---No se ha creado el TipoItem"
        print "\n --Buscar un TipoItem inexistente"
        valido = False
        valido = TipoItem.objects.filter(nombre_tipo_item="detallesExtras").exists()
        if valido==False:
            print "\n---No existe el TipoItem buscado"
