from django.test import TestCase
from django.test import Client
from publications.models import Publication
from users.models import User
#

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
            subscription=True,
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
            'content': 'content2',
            'is_paid': True
        }
        self.data3 = {
            'owner': self.user2.pk,
            'header': 'second',
            'content': 'content2',
            'is_paid': False
        }
        self.data2 = {
            'owner': "self.user",
            'header': 'second',
            'content': 'content2',
            'is_paid': True
        }
    def test_get_list_no_sub(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user)
        response = self.client.get(path='/publications/')
        self.assertEqual(response.status_code, 302)

    def test_get_list_sub(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user2)
        response = self.client.get(path='/publications/')
        self.assertEqual(response.status_code, 200)

    def test_get_list_sub_paid_posts(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user2)
        response = self.client.get(path='/paid_publications/')
        self.assertEqual(response.status_code, 200)

    def test_get_list_no_sub_paid_posts(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user)
        response = self.client.get(path='/paid_publications/')
        self.assertEqual(response.status_code, 302)

    def test_get_list_sub_free_posts(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user2)
        response = self.client.get(path='/free_publications/')
        self.assertEqual(response.status_code, 200)

    def test_get_list_no_sub_free_posts(self):
        """Тест вывода Публикаций без подписки"""
        self.client.force_login(user=self.user)
        response = self.client.get(path='/free_publications/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Тест"""
        self.client.force_login(user=self.user)
        response = self.client.post('/create-publication/', data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_post(self):
        """Тест"""
        self.client.force_login(user=self.user2)
        response = self.client.post('/create-publication/', data=self.data3)
        self.assertEqual(response.status_code, 302)

    def test_user_can_get(self):
        """Пользователь имеет доступ"""
        self.client.force_login(user=self.user)
        pk = Publication.objects.all()[0].pk
        response = self.client.get(f'/view-publication/{pk}/')
        self.assertEqual(response.status_code, 200)

    def test_base_get(self):
        """Редирект"""
        self.client.force_login(user=self.user)
        response = self.client.get(f'/success/')
        self.assertEqual(response.status_code, 302)

    def test_register_get(self):
        response = self.client.get(f'/email-register/')
        self.assertEqual(response.status_code, 200)

    def test_post_reg(self):
        response = self.client.post('/email-register/', data=self.data2)
        self.assertEqual(response.status_code, 200)

    def test_post_e(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/email-confirmed/')
        self.assertEqual(response.status_code, 200)

    def test_post_del_nosub(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/delete-publication/2/')
        self.assertEqual(response.status_code, 404)

    def test_post_del_sub(self):
        self.client.force_login(user=self.user2)
        response = self.client.get('/delete-publication/2/')
        self.assertEqual(response.status_code, 404)