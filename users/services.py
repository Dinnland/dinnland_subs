import stripe
from django.conf import settings


def get_session(instance):
    """Возаращаем сессию для оплаты курса или урока по API"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    product_name = str(instance.user) + str(instance.date_of_payment)
    product = stripe.Product.create(name=f'{product_name}')
    YOUR_DOMAIN = "http://127.0.0.1:8000"

    price = stripe.Price.create(
        unit_amount=instance.payment_amount,
        currency='rub',
        product=f'{product.id}'
    )

    session = stripe.checkout.Session.create(
        # payment_method_types=['card'],
        line_items=[
            {

                'price': f"{price.id}",
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
        # надеюсь сработает
        customer_email=f"{instance.user.email}",
    )

    return session


def retrieve_session(session):
    """ Возвращаем obj сессии по АПИ, id передаем в аргумент функц"""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    return stripe.checkout.Session.retrieve(session,)
