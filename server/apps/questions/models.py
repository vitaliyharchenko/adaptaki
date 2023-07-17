from django.db import models
from markdownx.models import MarkdownxField


def get_question_image_directory_path(instance, filename):
    return f'questions/question_{instance.pk}/{filename}'


# политики проверки
ONE_WRONG_MINUS_ONE = 1
ONE_WRONG_MINUS_ALL = 2

POLICY_CHOICES = [
    (ONE_WRONG_MINUS_ONE, 'Один неверный ответ, минус один балл.'),
    (ONE_WRONG_MINUS_ALL, 'Один неверный ответ, минус все баллы.'),
]

# типы заданий
SIMPLE = 1
ORDERED_SYMBOLS = 2
UNORDERED_SYMBOLS = 3
ONE_CHOICE = 4
MANY_CHOICE = 5
COMPOSITE = 6

TYPE_CHOICES = [
    (SIMPLE, 'Обычная проверка строки'),
    (ORDERED_SYMBOLS, 'Набор символов в строгом порядке'),
    (UNORDERED_SYMBOLS, 'Набор символов в случайном порядке'),
    (ONE_CHOICE, 'Выбор одного верного ответа (с кнопками)'),
    (MANY_CHOICE, 'Выбор нескольких вариантов ответа (с кнопками)'),
    (COMPOSITE, 'Развернутый ответ текстом или картинкой'),
]


# Модель задания
class Question(models.Model):
    # основное
    question_text = MarkdownxField(verbose_name='Текст вопроса')
    explanation_text = MarkdownxField(
        verbose_name='Комментарий (пояснение) к вопросу', blank=True)

    # картинки
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=get_question_image_directory_path,
        null=True,
        blank=True
    )
    explanation_image = models.ImageField(
        verbose_name='Картинка в пояснении',
        upload_to=get_question_image_directory_path,
        null=True,
        blank=True
    )

    # оценивание
    max_score = models.SmallIntegerField(
        verbose_name='Максимальный балл',
        default=1,
    )

    checking_policy = models.SmallIntegerField(
        verbose_name='Политика проверки заданий',
        choices=POLICY_CHOICES,
        default=ONE_WRONG_MINUS_ONE,
    )

    type = models.SmallIntegerField(
        verbose_name='Тип задания',
        choices=TYPE_CHOICES,
        default=1,
    )

    # For graph
    nodes = models.ManyToManyField(
        'graph.Node', blank=True, verbose_name="Вершины графа")

    # For exam tree
    trainer_tags = models.ManyToManyField(
        'trainer.TrainerTag', blank=True, verbose_name="Экзаменационный тег (old)")
    exam_tag = models.ForeignKey(
        'trainer.ExamTag', blank=True, null=True, verbose_name="Тег экзамена (new)", on_delete=models.SET_NULL, related_name='questions')

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

    def __str__(self):
        return f'#{self.pk}. {self.question_text[:30]}...'

    def all_options(self):
        opts = QuestionOption.objects.filter(question=self)
        return opts


def option_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/...
    return 'questions/question_{0}/options/{1}/{2}'.format(
        instance.question.pk,
        instance.pk,
        filename)


# вариант ответа
class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="option_question"
    )

    is_true = models.BooleanField(
        verbose_name='Правильный?',
        default=False
    )

    option_text = MarkdownxField(
        verbose_name='Текст варианта с разметкой',
        null=True,
        blank=True
    )

    # дополнительно
    option_image = models.ImageField(
        verbose_name='Картинка',
        upload_to=option_image_directory_path,
        null=True,
        blank=True
    )
    help_text = MarkdownxField(
        verbose_name='Подсказка',
        max_length=300,
        blank=True
    )

    class Meta:
        verbose_name = 'вариант ответа на задание'
        verbose_name_plural = 'варианты ответа на задания'

    def __str__(self):
        return self.option_text
