from django.test import TestCase, Client
from django.contrib.auth.models import User,Group
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import  NoSuchAttributeException, NoSuchElementException, NoAlertPresentException
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
        self.browser.implicitly_wait(3)

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


    def test_crear_y_borrar_usuario(self):
        self.browser.get(self.live_server_url)
        self.find_element_by_link_text("Iniciar Sesion").click()
        self.find_element_by_name("username").clear()
        self.find_element_by_name("username").send_keys("eduardo")
        self.find_element_by_name("password").clear()
        self.find_element_by_name("password").send_keys("edu")
        self.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Modulo de Administracion"))
        self.find_element_by_link_text("Modulo de Administracion").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Crear Usuario"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Listar Usuarios"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Crear Grupos"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Listar Grupos"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Asignar Roles"))
        self.find_element_by_link_text("Crear Usuario").click()
        self.find_element_by_id("id_username").clear()
        self.find_element_by_id("id_username").send_keys("edufd")
        self.find_element_by_id("id_password").clear()
        self.find_element_by_id("id_password").send_keys("12345")
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=id_groups | label=Administracion]]
        self.find_element_by_id("id_nombre").clear()
        self.find_element_by_id("id_nombre").send_keys("Eduardo")
        self.find_element_by_id("id_apellido").clear()
        self.find_element_by_id("id_apellido").send_keys("Florencio")
        self.find_element_by_id("id_ci").clear()
        self.find_element_by_id("id_ci").send_keys("223456")
        self.find_element_by_id("id_telefono").clear()
        self.find_element_by_id("id_telefono").send_keys("666987")
        self.find_element_by_name("submit").click()
        self.find_element_by_link_text("Retornar a la pagina de inicio").click()
        self.find_element_by_link_text("Usuarios").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "edufd"))
        self.find_element_by_link_text("Listar Usuarios").click()
        self.find_element_by_xpath("(//a[contains(text(),'Eliminar')])[2]").click()
        self.find_element_by_xpath("//input[@value='Si']").click()
        self.find_element_by_link_text("Logout").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
