from django.db import models


class Subject(models.Model):
    """
        Предмет: физика, математика, etc
    """
    title = models.CharField(
        verbose_name='Название предмета',
        max_length=300)

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self):
        return self.title


class Concept(models.Model):
    """
    Большая тема, объединяющая несколько вершин в подграф
    Пример: Квадратные уравнения
    """
    title = models.CharField(
        verbose_name='Название концепта',
        max_length=300)
    
    subject = models.ForeignKey(
        Subject,
        default=None,
        null=True,
        on_delete=models.SET_DEFAULT
    )

    is_active = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'концепт'
        verbose_name_plural = 'концепты'

    def __str__(self):
        return f"{self.pk}_{self.subject}_{self.concept}"


# Типы вершин графа
KNOW = 'KN'
UNDERSTAND = 'UN'
CASES = 'CS'
SKILLS = 'SK'
TYPE_CHOICES = [
    (KNOW, 'Понятие (знаю)'),
    (UNDERSTAND, 'Закономерность (понимаю)'),
    (CASES, 'Кейс (наблюдаю)'),
    (SKILLS, 'Навык (умею)')
]


class Node(models.Model):
    """
        Узел графа
    """
    title = models.CharField("Название узла", max_length=200)

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=KNOW,
        verbose_name='тип узла')

    subject = models.ForeignKey(
        Subject,
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name="Предмет"
    )

    concept = models.ForeignKey(
        Concept,
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
        verbose_name="Концепт"
    )

    testability = models.BooleanField(
        default=True,
        verbose_name="Проверяемая?"
    )

    class Meta:
        verbose_name = 'вершина графа'
        verbose_name_plural = 'вершины графа'

    def __str__(self):
        return str(self.title)

    def count_questions(self):
        questions = Question.objects.filter(nodes=self)
        return questions.count()

    def questions_list(self):
        questions = Question.objects.filter(nodes=self).values()
        return questions

    def delete(self, *args, **kwargs):

        super(Node, self).delete(*args, **kwargs)


class NodeRelation(models.Model):
    """
        Связь в графе
    """
    parent = models.ForeignKey(
        Node,
        related_name='parent_node',
        verbose_name='От вершины...',
        on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        Node,
        related_name='child_node',
        verbose_name='...к вершине',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'ребро в графе'
        verbose_name_plural = 'ребра в графе'
        unique_together = ('parent', 'child',)

    def __str__(self):
        return f"Ребро от {self.parent.title[:20]} к {self.child.title[:20]}"
