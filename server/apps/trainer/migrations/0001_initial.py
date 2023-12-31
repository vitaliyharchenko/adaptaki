# Generated by Django 4.2.3 on 2023-07-13 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название экзамена')),
            ],
            options={
                'verbose_name': 'экзамен',
                'verbose_name_plural': 'экзамены',
            },
        ),
        migrations.CreateModel(
            name='NumTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Заголовок группы тем экзамена')),
            ],
            options={
                'verbose_name': 'заголовок для номера из экзамена',
                'verbose_name_plural': 'заголовки для номеров из экзамена',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Тема задачи')),
            ],
            options={
                'verbose_name': 'тема задачи',
                'verbose_name_plural': 'темы задач',
            },
        ),
        migrations.CreateModel(
            name='TrainerTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(verbose_name='Номер задачи в кодификаторе')),
                ('is_active', models.BooleanField(default=True, verbose_name='Тег отображается?')),
                ('exam', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='trainer.exam', verbose_name='Экзамен')),
                ('num_title', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='trainer.numtitle', verbose_name='Название номера')),
                ('subject', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='graph.subject', verbose_name='Предмет')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.theme', verbose_name='Название темы')),
            ],
            options={
                'verbose_name': 'указатель на рубрикатор',
                'verbose_name_plural': 'указатели на рубрикатор',
            },
        ),
    ]
