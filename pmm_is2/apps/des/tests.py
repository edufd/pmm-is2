from django.test import TestCase
from django.contrib.auth.models import User, Group
from pmm_is2.apps.des.models import TipoItem, Atributo, Item
from pmm_is2.apps.adm.models import Proyecto, Fase



#./manage.py test modelos --desde consola
# Create your tests here.

class AtributoTestCase (TestCase):
   def setUp (self):
       print "\n TEST ATRIBUTO"
       print "\n --Buscar el atributo creado"
       tipo_item = TipoItem.objects.create(nombre_tipo_item="test tipo item", descripcion="aa")
       Atributo.objects.create(nombre_atributo_tipo_item="test atributo", tipo_atributo="NUMERICO",
                                obligatorio="SI",descripcion="aa",observacion="CC",
                                tipo_item=tipo_item)
   def test_traer(self):
       self.assertTrue(Atributo.objects.get(nombre_atributo_tipo_item="test atributo"))
   def test_Atributotraer(self):
       valido = False
       valido = Atributo.objects.filter(nombre_atributo_tipo_item="test atributo").exists()

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
        TipoItem.objects.create(nombre_tipo_item="test tipo item", descripcion="aa")

    def test_TipoItemtraer(self):
        valido = False
        valido = TipoItem.objects.filter(nombre_tipo_item="test tipo item").exists()
        if valido:
            print "\n---Se ha encontrado el TipoItem creado"
        if valido==False:
            print "\n---No se ha creado el TipoItem"
        print "\n --Buscar un TipoItem inexistente"
        valido = False
        valido = TipoItem.objects.filter(nombre_tipo_item="detallesExtras").exists()
        if valido==False:
            print "\n---No existe el TipoItem buscado"

class test_item_is_related_to_fase_and_tipo_item(TestCase):
    def setUp(self):
        usuario = User.objects.create(username="edu", password="edu")
        #grupos = Group.objects.create(name="Administrador")
        proyecto = Proyecto.objects.create(nombre_proyecto='Tv Chat', descripcion='Analisis de Requerimientos',
                                           presupuesto=3000000, estado_proyecto='NO-INICIADO',
                                           numero_fases=2, fecha_inicio='2014-05-11', fecha_fin='2014-05-31',
                                           plazo=21, lider_proyecto=usuario)
        tipo_item = TipoItem.objects.create(nombre_tipo_item="test tipo item", descripcion="aa")
        fase = Fase.objects.create(proyecto=proyecto, nombre_fase='Analisis',
                                   descripcion='Analisis de Requerimientos', estado_fase='ABIERTA',
                                   numero_secuencia=1)
        Atributo.objects.create(nombre_atributo_tipo_item="test atributo", tipo_atributo="NUMERICO",
                                obligatorio="SI",descripcion="aa",observacion="CC",
                                tipo_item=tipo_item)
        item = Item.objects.create(nombre_item="Test Item", prioridad="ALTA", estado="ACTIVO",
                            descripcion="Test Item", observaciones="Item for testing",
                            complejidad=5, costo=5000, id_tipo_item=tipo_item, id_fase=fase)
