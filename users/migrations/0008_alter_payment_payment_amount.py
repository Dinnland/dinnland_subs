# Generated by Django 4.2.6 on 2023-11-11 05:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_payment_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100)], verbose_name='сумма оплаты'),
        ),
    ]
