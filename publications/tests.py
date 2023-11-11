from django.test import TestCase
from django.urls import reverse
# from rest_framework import status
from django.contrib import auth
from django.test import Client
from publications.models import Publication
from users.models import User
# from django.test import override_settings, testcases
# from django.test.client import Client as DjangoClient
# from django.test.client import ClientHandler
# from django.test.client import RequestFactory as DjangoRequestFactory
from rest_framework.test import APITestCase, APIClient
# Create your tests here.

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000/login/')
        self.assertEqual(response.status_code, 200)


class TheTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000/login/')
        self.assertEqual(response.status_code, 200)


class PublicationTestCase(TestCase):
    def setUp(self):  # -> None:
        self.url = '/'
        """Создание пользователя"""
        self.user = User.objects.create(
            email='test@user.ru',
            phone='+79171717171',)
        self.user.set_password('00000000')
        self.user.save()

        self.user2 = User.objects.create(
            email='test@user2.ru',
            phone='+79170000000',
        )
        self.user.set_password('11111111')
        self.user.save()

        """Создание Публикации"""
        self.publication = Publication.objects.create(
            owner=self.user,
            header='first',
            content='content'
        )

        self.data = {
            'owner': self.user,
            'header': 'second',
            # 'course': self.course,
            'content': 'content2',
            # 'quantity_of_views': '2'
            'is_paid': True
        }
        self.wrongdata = {
            'owner': self.user,
            'header': 'second',
            # 'course': self.course,
            'content': 'content2',
            # 'quantity_of_views': '2'
            'is_paid': '3'
        }
        self.data2 = {
            'owner': "self.user",
            'header': 'second',
            # 'course': self.course,
            'content': 'content2',
            # 'quantity_of_views': '2'
            'is_paid': "True"
        }
    def test_get_list(self):
        """Тест вывода Публикаций"""
        self.client.force_login(user=self.user)
        response = self.client.get(path='/publications/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Тест, где все ОК"""
        # self.client.force_authenticate(user=self.user)
        self.client.force_login(user=self.user)
        response = self.client.post('/create-publication/', data=self.data)
        self.assertEqual(response.status_code, 302 )

    def test_user_can_get(self):
        """Пользователь имеет доступ"""
        self.client.force_login(user=self.user)

        pk = Publication.objects.all()[0].pk
        response = self.client.get(f'/view-publication/{pk}/')

        self.assertEqual(response.status_code, 200)

    def test_base_get(self):
        """Редирект"""
        self.client.force_login(user=self.user)

        # pk = Publication.objects.all()[0].pk
        response = self.client.get(f'/success/')

        self.assertEqual(response.status_code, 302)

    def test_register_get(self):

        # self.client.force_login(user=self.user)

        # pk = Publication.objects.all()[0].pk
        response = self.client.get(f'/email-register/')

        self.assertEqual(response.status_code, 200)

    def test_post_reg(self):
        # self.client.force_authenticate(user=self.user)
        # self.client.force_login(user=self.user)
        response = self.client.post('/email-register/', data=self.data2)
        self.assertEqual(response.status_code, 200 )

    def test_post_e(self):
        # self.client.force_authenticate(user=self.user)
        self.client.force_login(user=self.user)
        response = self.client.get('/email-confirmed/')
        self.assertEqual(response.status_code, 200 )
