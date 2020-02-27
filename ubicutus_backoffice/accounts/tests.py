from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import resolve
from django.urls import reverse
from .views import registerView
from .models import UserProfile
import re

# Create your tests here.

class AccountTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_registrar_usuario_post(self):
        url = 'http://127.0.0.1:8000/signup/'
        data = {
            'username': 'mgil@ubicutus.com',
            'email': 'ubimanu',
            'password1': '',
            'password2': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(registerView(data), True)

    def test_registrar_usuario_campos_vacios(self):
        url = 'http://127.0.0.1:8000/signup/'
        data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)

    ## Caso de Prueba Maliciosa
    # def test_registrar_usuario_sin_arroba_email(self):
    #     url = 'http://127.0.0.1:8000/login/'
    #     data = {
    #         'email': 'correo',
    #         'password1': '12345678',
    #         'password2': '12345678'
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(registrarUsuario(data['email'], data['password1'],data['password2']), False)
    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
