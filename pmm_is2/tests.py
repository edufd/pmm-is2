__author__ = 'Eduardo'
from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        print "\n TEST template de /"
        print "\n --Comprobar si carga el template de / "
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'pmm_is2/index.html')
