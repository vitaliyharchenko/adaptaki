# Generated by Django 4.2.3 on 2023-07-15 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0007_examtheme_is_active'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExamTheme',
            new_name='ExamTag',
        ),
    ]