# Generated by Django 4.2.3 on 2023-07-12 09:40

import apps.users.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=30, unique=True, verbose_name='Телефон')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Фамилия')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('is_active', models.BooleanField(default=True, verbose_name='Профиль активен?')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Права администратора')),
                ('class_of', models.CharField(blank=True, choices=[('parent', 'Родитель'), ('old', 'Выпускник'), ('2024', '11 класс'), ('2025', '10 класс'), ('2026', '9 класс'), ('2027', '8 класс'), ('2028', '7 класс')], max_length=10)),
                ('telegram_id', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Id в телеграм')),
                ('telegram_username', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Username в Telegram')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
            managers=[
                ('objects', apps.users.managers.UserManager()),
            ],
        ),
    ]
