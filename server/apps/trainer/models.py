from django.db import models
from apps.questions.models import Question


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
    exam = models.ForeignKey('trainer.Exam', on_delete=models.CASCADE, related_name='subject_exams')
    subject = models.ForeignKey(
        'graph.Subject', on_delete=models.CASCADE, related_name='subject_exams')

    class Meta:
        verbose_name = 'экзамен по предмету'
        verbose_name_plural = 'экзамены по предметам'

    def __str__(self):
        return f'{self.exam}, {self.subject}'

    def questions_exist(self):
        sens = SubjectExamNumber.objects.filter(subject_exam=self)
        counter = 0
        for sen in sens:
            counter += sen.questions_exist()
        return counter


class SubjectExamNumber(models.Model):
    subject_exam = models.ForeignKey(
        'trainer.SubjectExam', on_delete=models.CASCADE, related_name='subject_exam_numbers')
    num = models.SmallIntegerField(verbose_name='Номер задания')
    title = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'номер в экзамене по предмету'
        verbose_name_plural = 'номера в экзамене по предметам'

    def __str__(self):
        return f'{self.subject_exam}, №{self.num} {self.title}'

    def questions_exist(self):
        tags = ExamTag.objects.filter(subject_exam_number=self)
        counter = 0
        for tag in tags:
            counter += tag.questions_exist()
        return counter


class ExamTag(models.Model):
    """
        Тема задачи
    """
    title = models.CharField(
        verbose_name='Тема задачи',
        max_length=300)
    subject_exam_number = models.ForeignKey(
        'trainer.subjectexamnumber', null=True, on_delete=models.CASCADE, related_name='exam_tags')
    is_active = models.BooleanField(
        default=True,
        verbose_name="Тег отображается?"
    )

    class Meta:
        verbose_name = 'привязка к кодификатору'
        verbose_name_plural = 'привязки к кодификатору'

    def __str__(self):
        return f"{self.subject_exam_number} {self.title} {self.is_active}"

    def questions_exist(self):
        query = Question.objects.filter(exam_tag=self)
        return len(query)
