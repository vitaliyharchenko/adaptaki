# Generated by Django 4.2.3 on 2023-07-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0013_subjectexam_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectexamnumber',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
    ]