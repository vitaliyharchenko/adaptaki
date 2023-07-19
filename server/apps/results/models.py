from django.utils import timezone
from django.db import models
from model_utils.managers import InheritanceManager


class Result(models.Model):
    """
        Parent model for question result
    """
    question = models.ForeignKey(
        'questions.Question',
        related_name='results',
        on_delete=models.CASCADE,
        verbose_name='Задание'
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(default=timezone.now,
                                verbose_name='Дата ответа')
    score = models.IntegerField(default=0,
                                verbose_name='Количество баллов')
    max_score = models.IntegerField(default=0,
                                    verbose_name='Максимум баллов')
    
    # Ingeritance manager 
    # https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    class Meta:
        verbose_name = 'результат ученика'
        verbose_name_plural = 'результаты учеников'

    def __str__(self):
        return f'Result #{self.pk} Date: {self.date} Score: {self.score}'

    def set_score(self):
        pass


class StringResult(Result):
    """
        Model for result with string answer
    """
    answer = models.CharField(
        verbose_name='Ответ ученика',
        max_length=300,
        blank=False,
        default=None,
    )

    class Meta:
        verbose_name = 'ответ на вопрос строкой'
        verbose_name_plural = 'ответ на вопросы строкой'

    def __str__(self):
        return f'#{self.pk} Дата: {self.date} Балл: {self.score}/{self.max_score} Ответ:{self.answer[:30]} Пользователь: {self.user}'


# TODO: ответ ученика файлом
# class FileResult(Result):
