# Generated by Django 4.2.3 on 2023-07-17 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_remove_question_trainer_tags'),
        ('trainer', '0009_alter_examtag_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainertag',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='trainertag',
            name='num_title',
        ),
        migrations.RemoveField(
            model_name='trainertag',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='trainertag',
            name='theme',
        ),
        migrations.DeleteModel(
            name='NumTitle',
        ),
        migrations.DeleteModel(
            name='TrainerTag',
        ),
    ]