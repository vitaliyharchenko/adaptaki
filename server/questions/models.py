import json
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from graph.models import Node


class QuestionType(models.TextChoices):
    """Типы заданий"""
    STRING = 'STRING', 'Ответ строкой'
    NUMBER = 'NUMBER', 'Ответ числом'
    SEQUENCE_ORDERED = 'SEQ_ORDERED', 'Последовательность с порядком'
    SEQUENCE_UNORDERED = 'SEQ_UNORDERED', 'Последовательность без порядка'


class GradingPolicy(models.TextChoices):
    """Политики проверки"""
    ALL_OR_NOTHING = 'ALL_OR_NOTHING', 'Все или ничего'
    PER_ERROR = 'PER_ERROR', 'За каждую ошибку -1 балл'


class Question(models.Model):
    """Модель задачи"""
    title = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Название задачи (опционально)'
    )

    # Условие задачи
    condition = models.TextField(
        verbose_name='Условие задачи'
    )

    # Разбор задачи
    solution = models.TextField(
        blank=True,
        verbose_name='Разбор задачи'
    )

    # Тип задания
    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.STRING,
        verbose_name='Тип задания'
    )

    # Максимальный балл
    max_score = models.PositiveIntegerField(
        default=1,
        verbose_name='Максимальный балл'
    )

    # Политика проверки
    grading_policy = models.CharField(
        max_length=20,
        choices=GradingPolicy.choices,
        default=GradingPolicy.ALL_OR_NOTHING,
        verbose_name='Политика проверки'
    )

    # Привязка к узлам графа
    nodes = models.ManyToManyField(
        Node,
        blank=True,
        verbose_name='Связанные узлы графа'
    )

    # Аналогичные задачи
    analogs = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Аналогичные задачи'
    )

    # Метаданные
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна?'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    # Дополнительные поля для будущих типов
    precision = models.PositiveIntegerField(
        default=0,
        verbose_name='Точность (количество знаков после запятой)'
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or self.get_auto_title()

    def get_auto_title(self):
        """Автоматически генерирует название из условия"""
        if not self.condition:
            return f"Задача #{self.id}"

        # Убираем HTML теги и берем первые 100 символов
        import re
        clean_text = re.sub(r'<[^>]+>', '', self.condition)
        clean_text = clean_text.strip()

        if len(clean_text) <= 100:
            return clean_text
        else:
            return clean_text[:97] + "..."

    def clean(self):
        """Валидация модели"""
        super().clean()

        # Проверяем, что есть правильные варианты ответов
        correct_options = self.options.filter(is_correct=True)
        if not correct_options.exists():
            raise ValidationError(
                _('Необходимо указать хотя бы один правильный вариант ответа'))

        # Для заданий с множественным выбором проверяем количество правильных ответов
        if self.question_type == QuestionType.SEQUENCE_UNORDERED:
            if correct_options.count() < 2:
                raise ValidationError(
                    _('Для заданий с множественным выбором необходимо указать несколько правильных вариантов'))

    def get_correct_answers(self):
        """Получить все правильные ответы"""
        return list(self.options.filter(is_correct=True).values_list('text', flat=True))

    def get_options_shuffled(self):
        """Получить варианты ответов в случайном порядке"""
        return self.options.all().order_by('?')

    def check_answer(self, user_answer):
        """Проверить ответ пользователя"""
        if self.question_type == QuestionType.STRING:
            return self._check_string_answer(user_answer)
        elif self.question_type == QuestionType.NUMBER:
            return self._check_number_answer(user_answer)
        elif self.question_type == QuestionType.SEQUENCE_ORDERED:
            return self._check_ordered_sequence_answer(user_answer)
        elif self.question_type == QuestionType.SEQUENCE_UNORDERED:
            return self._check_unordered_sequence_answer(user_answer)
        else:
            return False, 0, "Неизвестный тип задания"

    def _check_string_answer(self, user_answer):
        """Проверка строкового ответа"""
        correct_answers = self.get_correct_answers()
        user_answer_clean = str(user_answer).strip().lower()

        is_correct = any(
            str(correct).strip().lower() == user_answer_clean
            for correct in correct_answers
        )

        score = self.max_score if is_correct else 0
        feedback = "Правильно!" if is_correct else f"Правильный ответ: {', '.join(correct_answers)}"

        return is_correct, score, feedback

    def _check_number_answer(self, user_answer):
        """Проверка числового ответа"""
        try:
            user_num = float(user_answer)
            correct_answers = self.get_correct_answers()

            is_correct = any(
                abs(user_num - float(correct)) < 0.001  # Небольшая погрешность
                for correct in correct_answers
            )

            score = self.max_score if is_correct else 0
            feedback = "Правильно!" if is_correct else f"Правильный ответ: {', '.join(correct_answers)}"

            return is_correct, score, feedback
        except (ValueError, TypeError):
            return False, 0, "Ответ должен быть числом"

    def _check_ordered_sequence_answer(self, user_answer):
        """Проверка последовательности с порядком"""
        if not isinstance(user_answer, list):
            return False, 0, "Ответ должен быть списком"

        correct_answers = self.get_correct_answers()
        user_answer_str = ','.join(map(str, user_answer))

        is_correct = user_answer_str in correct_answers
        score = self.max_score if is_correct else 0
        feedback = "Правильно!" if is_correct else f"Правильный ответ: {', '.join(correct_answers)}"

        return is_correct, score, feedback

    def _check_unordered_sequence_answer(self, user_answer):
        """Проверка последовательности без порядка"""
        if not isinstance(user_answer, list):
            return False, 0, "Ответ должен быть списком"

        correct_answers = self.get_correct_answers()
        user_answer_str = ','.join(map(str, sorted(user_answer)))

        is_correct = any(
            ','.join(map(str, sorted(correct.split(',')))) == user_answer_str
            for correct in correct_answers
        )

        if self.grading_policy == GradingPolicy.ALL_OR_NOTHING:
            score = self.max_score if is_correct else 0
        else:
            # Подсчитываем количество правильных элементов
            if is_correct:
                score = self.max_score
            else:
                # Находим максимальное совпадение с любым правильным ответом
                max_correct = 0
                for correct in correct_answers:
                    correct_list = [int(x.strip()) for x in correct.split(',')]
                    user_set = set(user_answer)
                    correct_set = set(correct_list)
                    intersection = len(user_set & correct_set)
                    max_correct = max(max_correct, intersection)

                score = int((max_correct / len(correct_list)) *
                            self.max_score) if correct_list else 0

        feedback = "Правильно!" if is_correct else f"Правильный ответ: {', '.join(correct_answers)}"
        return is_correct, score, feedback


class QuestionOption(models.Model):
    """Вариант ответа на задание"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Задача'
    )

    text = models.TextField(
        verbose_name='Текст варианта'
    )

    is_correct = models.BooleanField(
        default=False,
        verbose_name='Правильный ответ?'
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    class Meta:
        verbose_name = 'вариант ответа'
        verbose_name_plural = 'варианты ответов'
        ordering = ['order', 'id']
        unique_together = ['question', 'order']

    def __str__(self):
        return f"{self.question.title} - {self.text[:50]}"

    def clean(self):
        """Валидация варианта ответа"""
        super().clean()

        # Проверяем, что текст не пустой
        if not self.text.strip():
            raise ValidationError(
                _('Текст варианта ответа не может быть пустым'))
