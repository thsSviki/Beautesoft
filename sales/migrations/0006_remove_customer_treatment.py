# Generated by Django 3.0.5 on 2020-04-30 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_customer_topup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='treatment',
        ),
    ]
