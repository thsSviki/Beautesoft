# Generated by Django 3.0.5 on 2020-04-30 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_auto_20200430_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='salon',
        ),
    ]