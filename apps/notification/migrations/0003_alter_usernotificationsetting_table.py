# Generated by Django 3.2.5 on 2023-01-24 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20230124_1426'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='usernotificationsetting',
            table='user_notification_setting',
        ),
    ]
