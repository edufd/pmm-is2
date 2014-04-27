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

    def test_crear_y_borrar_usuario(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text("Iniciar Sesion").click()
        self.browser.find_element_by_name("username").clear()
        self.browser.find_element_by_name("username").send_keys("pmm")
        self.browser.find_element_by_name("password").clear()
        self.browser.find_element_by_name("password").send_keys("pmm2014")
        self.browser.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Modulo de Administracion"))
        self.browser.find_element_by_link_text("Modulo de Administracion").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Crear Usuario"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Listar Usuarios"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Crear Grupos"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Listar Grupos"))
        self.browser.implicitly_wait(3)
        self.browser.find_element_by_link_text("Crear Usuario").click()
        self.browser.find_element_by_id("id_username").clear()
        self.browser.find_element_by_id("id_username").send_keys("edufd")
        self.browser.find_element_by_id("id_password").clear()
        self.browser.find_element_by_id("id_password").send_keys("12345")
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=id_groups | label=Administracion]]
        self.browser.find_element_by_id("id_nombre").clear()
        self.browser.find_element_by_id("id_nombre").send_keys("Eduardo")
        self.browser.find_element_by_id("id_apellido").clear()
        self.browser.find_element_by_id("id_apellido").send_keys("Florencio")
        self.browser.find_element_by_id("id_ci").clear()
        self.browser.find_element_by_id("id_ci").send_keys('2223456')
        self.browser.find_element_by_id("id_telefono").clear()
        self.browser.find_element_by_id("id_telefono").send_keys('661538')
        self.browser.find_element_by_name("submit").click()
        self.browser.find_element_by_link_text("Retornar a la pagina de inicio").click()
        self.browser.find_element_by_link_text("Usuarios").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "edufd"))
        self.browser.find_element_by_link_text("Listar Usuarios").click()
        self.browser.find_element_by_xpath("(//a[contains(text(),'Eliminar')])[2]").click()
        self.browser.find_element_by_xpath("//input[@value='Si']").click()
        self.browser.find_element_by_link_text("Logout").click()

    def is_element_present(self, how, what):
        try: self.browser.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.browser.switch_to.alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.browser.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
