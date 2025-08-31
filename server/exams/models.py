from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class ExamType(models.Model):
    """Типы экзаменов (ЕГЭ, ОГЭ, Олимпиада и т.д.)"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название экзамена'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен?'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'тип экзамена'
        verbose_name_plural = 'типы экзаменов'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_subjects(self):
        """Получить предметы для данного экзамена"""
        return self.examsubjects.filter(is_active=True).order_by('order')


class ExamSubject(models.Model):
    """Связь экзамена с предметом"""
    exam_type = models.ForeignKey(
        ExamType,
        on_delete=models.CASCADE,
        related_name='examsubjects',
        verbose_name='Тип экзамена'
    )
    subject = models.ForeignKey(
        'graph.Subject',
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен?'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'предмет экзамена'
        verbose_name_plural = 'предметы экзаменов'
        ordering = ['order', 'subject__title']
        unique_together = ['exam_type', 'subject']

    def __str__(self):
        return f"{self.exam_type.name} - {self.subject.title}"

    def get_numbers(self):
        """Получить номера заданий для данного предмета"""
        return self.examnumbers.filter(is_active=True).order_by('order')


class ExamNumber(models.Model):
    """Номера заданий в экзамене"""
    exam_subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name='examnumbers',
        verbose_name='Предмет экзамена'
    )
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Номер задания'
    )
    title = models.CharField(
        max_length=300,
        verbose_name='Название задания'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно?'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'номер задания'
        verbose_name_plural = 'номера заданий'
        ordering = ['order', 'number']
        unique_together = ['exam_subject', 'number']

    def __str__(self):
        return f"Задание {self.number}. {self.title}"

    def get_topics(self):
        """Получить подтемы для данного номера задания"""
        return self.examtopics.filter(is_active=True).order_by('order')

    def get_full_path(self):
        """Получить полный путь к заданию"""
        return f"{self.exam_subject.exam_type.name} → {self.exam_subject.subject.title} → Задание {self.number}"


class ExamTopic(models.Model):
    """Подтемы внутри задания"""
    exam_number = models.ForeignKey(
        ExamNumber,
        on_delete=models.CASCADE,
        related_name='examtopics',
        verbose_name='Номер задания'
    )
    title = models.CharField(
        max_length=300,
        verbose_name='Название подтемы'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна?'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'подтема экзамена'
        verbose_name_plural = 'подтемы экзаменов'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_questions(self):
        """Получить задачи для данной подтемы"""
        return self.question_set.filter(is_active=True)

    def get_questions_count(self):
        """Получить количество задач для данной подтемы"""
        return self.question_set.filter(is_active=True).count()

    def get_full_path(self):
        """Получить полный путь к подтеме"""
        exam_path = self.exam_number.get_full_path()
        return f"{exam_path} → {self.title}"

    def get_full_path(self):
        """Получить полный путь к подтеме"""
        exam_path = self.exam_number.get_full_path()
        return f"{exam_path} → {self.title}"
