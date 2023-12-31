# Generated by Django 4.2.3 on 2023-07-17 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
        ('trainer', '0008_rename_examtheme_examtag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examtag',
            options={'verbose_name': 'тема задачи (NEW)', 'verbose_name_plural': 'темы задач (NEW)'},
        ),
        migrations.AlterField(
            model_name='examtag',
            name='subject_exam_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_tags', to='trainer.subjectexamnumber'),
        ),
        migrations.AlterField(
            model_name='subjectexam',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_exams', to='graph.subject'),
        ),
        migrations.AlterField(
            model_name='subjectexamnumber',
            name='subject_exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_exam_numbers', to='trainer.subjectexam'),
        ),
    ]
