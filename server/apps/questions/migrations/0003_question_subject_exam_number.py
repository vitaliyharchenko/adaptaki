# Generated by Django 4.2.3 on 2023-07-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0004_alter_subjectexamnumber_title'),
        ('questions', '0002_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subject_exam_number',
            field=models.ManyToManyField(blank=True, to='trainer.subjectexamnumber', verbose_name='Привязка к заданию экзамена'),
        ),
    ]