from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(phone='+71234567891', password='0000')
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
        admin_user = User.objects.create_superuser('+77777777777', '7777')
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

