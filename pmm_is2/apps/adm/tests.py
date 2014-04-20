from django.test import TestCase, Client
from django.contrib.auth.models import User,Group
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import  NoSuchAttributeException
from selenium.webdriver.common.by  import  By



#browser = webdriver.Firefox()
#browser.get('http://localhost:8000/')
#body = browser.find_element_by_tag_name('body')
#assert 'Django' in body.text
#browser.quit()

class UserTest(TestCase):
    fixtures = ['permisos.json','grupos.json','usuarios.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_coolness(self):
        self.assertEqual(4, len(User.objects.all()))

class AdminTest(LiveServerTestCase):

# load fixtures
    fixtures = ['permisos.json','grupos.json','usuarios.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_admin_site(self):
        #Entrar en la pagina de inicio
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('PMM', body.text)
        #Entrar en el login
        self.browser.get(self.live_server_url + '/login/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Iniciar Sesion', body.text)
        #Ingresar los datos del usuario
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('pmm')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('pmm2014')
        password_field.submit()
        #Entrar el menu principal
        body1 = self.browser.find_element_by_tag_name('body')
        self.assertIn('Proyectos Activos', body1.text)
        moduloAdministracion_link = self.browser.find_elements_by_link_text('Modulo de Administracion')
        moduloAdministracion_link[0].click()
        body = self.browser.find_element_by_tag_name('h1')#error