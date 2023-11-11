from rest_framework import serializers
from users.models import Payment, User
from users.services import retrieve_session


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print('create new user:')
        print(validated_data)
        return User.objects.create_user(**validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='phone', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ('session', 'user', 'payment_amount', 'date_of_payment', 'is_paid')


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    """this PaymentRetrieveSerializer"""
    user = UserSerializer(read_only=True)

    url_for_pay = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment

        fields = ('is_paid', 'date_of_payment', 'payment_amount',
                  'url_for_pay', 'session', 'user')

    def get_url_for_pay(self, instance) -> None | str | dict:
        """Возвращаем ссылку на оплату, если срок сессии прошел, либо оплачено -> None"""

        if instance.is_paid:
            return None
        session = retrieve_session(instance.session)
        if session.payment_status == 'unpaid' and session.status == 'open':
            return session.url
        elif session.payment_status == 'paid' and session.status == 'complete':
            return None
        status = {
            "session": "Срок сессии вышел! Необходимо заново создать платеж"
        }
        return status
