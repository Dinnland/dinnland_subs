from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создание учетных записей обычных пользователей"""
        # 1
        user = User.objects.create(
            email='test1@test1.ru',
            phone='1234567899',
            country='Kazan',
            first_name='Ilshat',
            last_name='Molodov'
        )
        user.set_password('1111')
        user.save()

        # 2
        user = User.objects.create(
            email='test2@test2.ru',
            phone='89176666667',
            country='USA',
            first_name='OLeg',
            last_name='Tinkoff'
        )
        user.set_password('2222')
        user.save()
