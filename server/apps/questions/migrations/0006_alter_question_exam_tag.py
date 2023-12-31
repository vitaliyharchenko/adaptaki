# Generated by Django 4.2.3 on 2023-07-17 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0008_rename_examtheme_examtag'),
        ('questions', '0005_remove_question_subject_exam_numbers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='exam_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='trainer.examtag', verbose_name='Тег экзамена (new)'),
        ),
    ]
