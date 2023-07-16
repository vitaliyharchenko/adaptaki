from django.db import models


class Exam(models.Model):
    """
        Экзамен: ЕГЭ, ОГЭ, etc
    """
    title = models.CharField(
        verbose_name='Название экзамена',
        max_length=300)

    class Meta:
        verbose_name = 'вид экзамена'
        verbose_name_plural = 'виды экзаменов'

    def __str__(self):
        return self.title


class SubjectExam(models.Model):
    exam = models.ForeignKey('trainer.Exam', on_delete=models.CASCADE)
    subject = models.ForeignKey('graph.Subject', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'экзамен по предмету'
        verbose_name_plural = 'экзамены по предметам'

    def __str__(self):
        return f'{self.exam}, {self.subject}'


class SubjectExamNumber(models.Model):
    subject_exam = models.ForeignKey(
        'trainer.SubjectExam', on_delete=models.CASCADE)
    num = models.SmallIntegerField(verbose_name='Номер задания')
    title = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'номер в экзамене по предмету'
        verbose_name_plural = 'номера в экзамене по предметам'

    def __str__(self):
        return f'{self.subject_exam}, №{self.num} {self.title}'


# Deprecated
class NumTitle(models.Model):
    """
        Заголовок группы заданий под одним номером
        Часто связан с номером задачи в кодификаторе
    """
    title = models.CharField(
        verbose_name='Заголовок группы тем экзамена',
        max_length=300)

    class Meta:
        verbose_name = 'заголовок для номера из экзамена'
        verbose_name_plural = 'заголовки для номеров из экзамена'

    def __str__(self):
        return str(self.title)


class ExamTag(models.Model):
    """
        Тема задачи
    """
    title = models.CharField(
        verbose_name='Тема задачи',
        max_length=300)
    subject_exam_number = models.ForeignKey(
        'trainer.subjectexamnumber', null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Тег отображается?"
    )

    class Meta:
        verbose_name = 'тема задачи (NEW)'
        verbose_name_plural = 'темы задач (NEW)'

    def __str__(self):
        return f"{self.subject_exam_number} {self.title} {self.is_active}"


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
        ExamTag,
        on_delete=models.CASCADE,
        verbose_name="Название темы"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Тег отображается?"
    )

    class Meta:
        verbose_name = 'указатель на рубрикатор'
        verbose_name_plural = 'указатели на рубрикатор'

    def __str__(self):
        return f"{self.exam}_{self.subject}_{self.num}_{self.theme}"
