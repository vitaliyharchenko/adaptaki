from django.db import models


class Exam(models.Model):
    """
        Экзамен: ЕГЭ, ОГЭ, etc
    """
    title = models.CharField(
        verbose_name='Название экзамена',
        max_length=300)

    class Meta:
        verbose_name = '1. экзамен'
        verbose_name_plural = '1. экзамены'

    def __str__(self):
        return self.title


class NumTitle(models.Model):
    """
        Заголовок группы заданий под одним номером
        Часто связан с номером задачи в кодификаторе
    """
    title = models.CharField(
        verbose_name='Заголовок группы тем экзамена',
        max_length=300)

    class Meta:
        verbose_name = '2. заголовок для номера из экзамена'
        verbose_name_plural = '2. заголовки для номеров из экзамена'

    def __str__(self):
        return str(self.title)


class Theme(models.Model):
    """
        Тема задачи
    """
    title = models.CharField(
        verbose_name='Тема задачи',
        max_length=300)

    class Meta:
        verbose_name = '3. тема задачи'
        verbose_name_plural = '3. темы задач'

    def __str__(self):
        return str(self.title)


class TrainerTag(models.Model):
    """
        Тэг-указатель на экзамен, предмет, номер задачи, заголовок номера (или ничего)
        ЕГЭ
        Математика
        1 номер
        * Заголовок номера (простые текстовые задачи), может быть пустым
        Название темы (элементарные вычисления), обязательное поле
    """
    exam = models.ForeignKey(
        Exam,
        default=None,
        null=True,
        on_delete=models.SET_DEFAULT,
        verbose_name="Экзамен"
    )

    subject = models.ForeignKey(
        'graph.Subject',
        default=None,
        null=True,
        on_delete=models.SET_DEFAULT,
        verbose_name="Предмет"
    )

    num = models.IntegerField(
        verbose_name='Номер задачи в кодификаторе',
    )

    num_title = models.ForeignKey(
        NumTitle,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT,
        verbose_name="Название номера"
    )

    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        verbose_name="Название темы"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Тег отображается?"
    )

    class Meta:
        verbose_name = '4. указатель на рубрикатор'
        verbose_name_plural = '4. указатели на рубрикатор'

    def __str__(self):
        return f"{self.exam}_{self.subject}_{self.num}_{self.theme}"
