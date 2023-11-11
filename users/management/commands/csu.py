from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создание учетной записи администратора django"""
        user = User.objects.create(
            email='dinn.land@maifl.ru',
            phone='+79171717171',
            first_name='Admin',
            last_name='Dinn',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('catalog1')
        user.save()
