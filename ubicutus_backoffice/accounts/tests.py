from django.test import TestCase

from django.contrib.auth.models import User
from .forms import SignUpForm,  EditUserDataForm, EditProfileForm
from django.urls import resolve
from django.urls import reverse
from .views import registerView
from .models import UserProfile
from django.core.validators import validate_email as VALIDATE_THE_EMAIL
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
import re

# Create your tests here.

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['first_name', 'last_name', 'username', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'manuel',
            'email': 'mgil@ubicutus.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('dashboard')
        self.login_url = reverse('login')

    # def test_redirection(self):
    #     '''
    #     A valid form submission should redirect the user to the home page
    #     '''
    #     self.assertRedirects(self.response, self.login_url)

    # def test_user_creation(self):
    #     self.assertTrue(User.objects.exists())

    # def test_user_authentication(self):
    #     '''
    #     Create a new request to an arbitrary page.
    #     The resulting response should now have a `user` to its context,
    #     after a successful sign up.
    #     '''
    #     response = self.client.get(self.home_url)
    #     user = response.context.get('user')
    #     self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
