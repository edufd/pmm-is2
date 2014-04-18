
#./manage test adm en consola
from django.test import TestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

#browser = webdriver.Firefox()
#browser.get('http://localhost:8000/')
#body = browser.find_element_by_tag_name('body')
#assert 'Django' in body.text
#browser.quit()
class AdminTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_admin_site(self):
    # user opens web browser, navigates to admin page
        #self.browser.get(self.live_server_url + '//')
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('PMM', body.text)

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'adriana'
        self.email = 'test@test.com'
        self.password = 'adrisila'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_login_exitoso(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

