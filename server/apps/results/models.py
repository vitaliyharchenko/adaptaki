from django.utils import timezone
from django.db import models


class Result(models.Model):
    """
        Parent model for question result
    """
    question = models.ForeignKey(
        'questions.Question',
        related_name='results',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'результат ученика'
        verbose_name_plural = 'результаты учеников'

    def __str__(self):
        return f'Result #{self.pk} Date: {self.date} Score: {self.score}'

    def set_score(self):
        # self.score = self.question.check_answer(self.answer)
        # self.save()
        # self.user_task_relation.score += self.score
        # self.user_task_relation.save()
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
        verbose_name = 'ответ на вопрос с ответом строкой'
        verbose_name_plural = 'ответ на вопросы с ответом строкой'

    def __str__(self):
        return f'Result #{self.pk} Date: {self.date} Score: {self.score} Answer:{self.answer[:30]}'


class ChoiceResult(Result):
    """
        Model for result with many answer options
    """
    answer = models.JSONField(
        verbose_name='Ответ ученика'
    )

    class Meta:
        verbose_name = 'ответ на вопрос с ответом выбором'
        verbose_name_plural = 'ответы на вопрос с ответом выбором'

    def __str__(self):
        return f'Result #{self.pk} Date: {self.date} Score: {self.score} Answer:{self.answer}'


# TODO: ответ ученика файлом
# class FileResult(Result):
