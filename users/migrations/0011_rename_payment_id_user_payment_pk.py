# Generated by Django 4.2.6 on 2023-11-11 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_payment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='payment_id',
            new_name='payment_pk',
        ),
    ]
