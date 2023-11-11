import time

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

from users.models import User


# Create your tests here.


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(phone='+71234567891', password='0000', email='user@1.com')
        self.assertEqual(user.phone, '+71234567891')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        # with self.assertRaises(TypeError):
        #     User.objects.create_user()
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(phone='')
        # with self.assertRaises(ValueError):
        #     User.objects.create_user(phone='', password="0000")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(phone='+77777777777', password='7777', email='user@777.com', )
        self.assertEqual(admin_user.phone, '+77777777777')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone='+77777777777', password='7777', is_superuser=False)


class UserTestCase(TestCase):
    client_class = Client
    def setUp(self):
        # self.url = '/'
        self.user = User.objects.create(
            email='test@user.ru',
            phone='+79171717171', )
        self.user.set_password('00000000')
        self.user.save()

        self.user2 = User.objects.create(
            email='test@user2.ru',
            phone='+79170000000',
        )
        self.user.set_password('11111111')
        self.user.save()

    def test_login(self):
        c = Client()
        response = c.post('/login/', {'username': self.user.phone, 'password': self.user.password})
        print(response.status_code)
        # response = c.get('/profile/')
        # print(response.content)
        self.assertEqual(response.status_code, 200)

class ModelsTestCase(TestCase):
    pass


class UsersTestCase(TestCase):
    def setUp(self):  # -> None:
        self.url = '/'
        """Создание пользователя"""
        self.user = User.objects.create(
            email='test@user.ru',
            phone='+79170000012',
            is_active=True,
            is_verified=True)
        self.user.set_password('00000000')
        self.user.save()

        self.user2 = User.objects.create(
            email='test@user2.ru',
            phone='+79170000000',
        )
        self.user.set_password('11111111')
        self.user.save()

        self.data_us_mail_rep = {
            'phone':'+79170000000',
        }
        self.data_us_mail_rep2 = {
            'phone': '+79171717551',
        }


    def test_get_list(self):
        """Тест без номера платежа закрыт доступ"""
        self.client.force_login(user=self.user)
        response = self.client.get(path=f'/profile/{self.user.pk}/{self.user.payment_pk}')
        self.assertEqual(response.status_code, 404 )

    def test_post_phone(self):
        """Тест, нельзя поменять номер, который есть в бд"""
        self.client.force_login(user=self.user)
        response = self.client.post(path=f'/profile/', data=self.data_us_mail_rep)
        self.assertNotEquals(str(self.user.phone), second=self.data_us_mail_rep['phone'] )

    def test_post_access(self):
        """Тест, Новый пароль по access коду"""
        # self.client.force_login(user=self.user)
        # response = self.client.post(path=f'/make-access-for-password/', data={'username': f'{self.user.phone}'})
        self.client.post(path=f'/make-access-for-password/', data={'id_username': f'{self.user.phone}'})
        # self.assertEquals(response, second=200 )

        old_pass = self.user.password
        print('userchik',self.user)
        print(old_pass)
        print('access_code---',self.user.access_code)
        self.client.post(path=f'/check-access-for-password/', data={'username': f'{self.user.phone}',
                                                                               'access_code': f'{self.user.access_code}'})
        new_pass = self.user.password
        print(new_pass)
        print('access_code---', self.user.access_code)
        self.assertEquals(old_pass, second=new_pass )

    def test_post_pass_email_refresh(self):
        """Тест, Новый пароль по email"""
        old_pass = self.user.password
        response = self.client.force_login(user=self.user)

        # response = self.client.post(path=f'/make-access-for-password/', data={'username': f'{self.user.phone}'})
        response = self.client.get(path='/profile/genpassword/')
        self.assertEquals(response.status_code, second=302)
        response = self.client.get(path='/done-generate-new-password/')
        new_pass = self.user.password
        self.assertEquals(old_pass, second=new_pass)


    # def test_post(self):
    #     """Тест, где все ОК"""
    #     # self.client.force_authenticate(user=self.user)
    #     self.client.force_login(user=self.user)
    #     response = self.client.post('/create-publication/', data=self.data)
    #     self.assertEqual(response.status_code, 302 )