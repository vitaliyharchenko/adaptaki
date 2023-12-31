# Generated by Django 4.2.3 on 2023-07-13 09:10

import apps.questions.models
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('graph', '0001_initial'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', markdownx.models.MarkdownxField(verbose_name='Текст вопроса')),
                ('explanation_text', markdownx.models.MarkdownxField(blank=True, verbose_name='Комментарий (пояснение) к вопросу')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.questions.models.get_question_image_directory_path, verbose_name='Картинка')),
                ('explanation_image', models.ImageField(blank=True, null=True, upload_to=apps.questions.models.get_question_image_directory_path, verbose_name='Картинка в пояснении')),
                ('max_score', models.SmallIntegerField(default=1, verbose_name='Максимальный балл')),
                ('checking_policy', models.SmallIntegerField(choices=[(1, 'Один неверный ответ, минус один балл.'), (2, 'Один неверный ответ, минус все баллы.')], default=1, verbose_name='Политика проверки заданий')),
                ('nodes', models.ManyToManyField(blank=True, to='graph.node', verbose_name='Вершины графа')),
                ('trainer_tags', models.ManyToManyField(blank=True, to='trainer.trainertag', verbose_name='Экзаменационный тег')),
            ],
            options={
                'verbose_name': 'задание',
                'verbose_name_plural': 'задания',
            },
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_true', models.BooleanField(default=False, verbose_name='Правильный?')),
                ('option_text', markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Текст варианта с разметкой')),
                ('option_image', models.ImageField(blank=True, null=True, upload_to=apps.questions.models.option_image_directory_path, verbose_name='Картинка')),
                ('help_text', markdownx.models.MarkdownxField(blank=True, max_length=300, verbose_name='Подсказка')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_question', to='questions.question')),
            ],
            options={
                'verbose_name': 'вариант ответа на задание',
                'verbose_name_plural': 'варианты ответа на задания',
            },
        ),
    ]
