# Generated by Django 4.2.3 on 2023-07-15 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0004_alter_subjectexamnumber_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Theme',
            new_name='ExamTheme',
        ),
    ]
