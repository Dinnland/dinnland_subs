from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """Юзер менеджер для создания пользователей"""
    use_in_migrations = True

    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError("The given username must be set")
    #     email = self.normalize_email(email)
    #     GlobalUserModel = apps.get_model(
    #         self.model._meta.app_label, self.model._meta.object_name
    #     )
    #     email = GlobalUserModel.normalize_username(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.password = make_password(password)
    #     user.save(using=self._db)
    #     return user

    # def _create_user(self, email=None, phone=None, password, **extra_fields):
    #     if not email and not phone:
    #         raise ValueError("The given username must be set: email or phone")
    #     if email:
    #         # print('_email hui')
    #         # print('email', email)
    #         # print('phone', phone)
    #         email = self.normalize_email(email)
    #         GlobalUserModel = apps.get_model(
    #             self.model._meta.app_label, self.model._meta.object_name
    #         )
    #         email = GlobalUserModel.normalize_username(email)
    #         user = self.model(email=email, **extra_fields)
    #         user.password = make_password(password)
    #         user.save(using=self._db)
    #         return user
    #     if phone:
    #         # print('_ph hui')
    #         # print('email', email)
    #         # print('phone', phone)
    #         # email = self.normalize_email(email)
    #         GlobalUserModel = apps.get_model(
    #             self.model._meta.app_label, self.model._meta.object_name
    #         )
    #         # email = GlobalUserModel.normalize_username(email)
    #         user = self.model(phone=phone, **extra_fields)
    #         user.password = make_password(password)
    #         user.save(using=self._db)
    #         return user

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given username must be set")
        # email = self.normalize_email(phone)
        phone = str(phone)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        phone = GlobalUserModel.normalize_username(phone)
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", False)
    #     extra_fields.setdefault("is_superuser", False)
    #     return self._create_user(email, password, **extra_fields)

    # def create_user(self, email = None, phone = None, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", False)
    #     extra_fields.setdefault("is_superuser", False)
    #     if email:
    #         # print('email hui')
    #         # print('email', email)
    #         # print('phone', phone)
    #         return self._create_user(email, password, **extra_fields)
    #     if phone:
    #         # print('ph hui')
    #         # print('email', email)
    #         # print('phone', phone)
    #         return self._create_user(phone, password, **extra_fields)

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #     extra_fields.setdefault("is_active", True)
    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError("Superuser must have is_staff=True.")
    #     if extra_fields.get("is_superuser") is not True:
    #         raise ValueError("Superuser must have is_superuser=True.")
    #     return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email = None, phone = None, password=None, **extra_fields):
    #
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #     extra_fields.setdefault("is_active", True)
    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError("Superuser must have is_staff=True.")
    #     if extra_fields.get("is_superuser") is not True:
    #         raise ValueError("Superuser must have is_superuser=True.")
    #     if email:
    #         return self._create_user(email, password, **extra_fields)
    #     if phone:
    #         return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, password, **extra_fields)

