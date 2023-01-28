# Generated by Django 3.2.5 on 2023-01-24 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotificationSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_re_notification', models.BooleanField(default=True)),
                ('order_re_notification', models.BooleanField(default=True)),
                ('updates', models.BooleanField(default=True)),
                ('new_user_reg', models.BooleanField(default=True)),
                ('order_failure', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='NOTIFICATION',
        ),
    ]
