from rest_framework import serializers
from .models import Question, QuestionOption, QuestionType, GradingPolicy
from graph.serializers import NodeSerializer


class QuestionOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для вариантов ответов"""

    class Meta:
        model = QuestionOption
        fields = ['id', 'text', 'is_correct', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для задач"""
    options = QuestionOptionSerializer(many=True, read_only=True)
    nodes = NodeSerializer(many=True, read_only=True)
    analogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    correct_answers_count = serializers.ReadOnlyField()
    options_count = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'condition', 'solution', 'question_type',
            'max_score', 'grading_policy', 'precision', 'is_active',
            'created_at', 'updated_at', 'options', 'nodes', 'analogs',
            'correct_answers_count', 'options_count'
        ]
        read_only_fields = ['created_at', 'updated_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задач"""
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'title', 'condition', 'solution', 'question_type',
            'max_score', 'grading_policy', 'precision', 'is_active',
            'nodes', 'analogs', 'options'
        ]

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        nodes_data = validated_data.pop('nodes', [])
        analogs_data = validated_data.pop('analogs', [])

        question = Question.objects.create(**validated_data)

        # Создаем варианты ответов
        for option_data in options_data:
            QuestionOption.objects.create(question=question, **option_data)

        # Устанавливаем связи
        question.nodes.set(nodes_data)
        question.analogs.set(analogs_data)

        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        nodes_data = validated_data.pop('nodes', [])
        analogs_data = validated_data.pop('analogs', [])

        # Обновляем основную модель
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем варианты ответов
        if options_data:
            # Удаляем старые варианты
            instance.options.all().delete()
            # Создаем новые
            for option_data in options_data:
                QuestionOption.objects.create(question=instance, **option_data)

        # Обновляем связи
        instance.nodes.set(nodes_data)
        instance.analogs.set(analogs_data)

        return instance


class QuestionAnswerSerializer(serializers.Serializer):
    """Сериализатор для ответов на задачи"""
    answer = serializers.JSONField()

    def validate_answer(self, value):
        """Валидация ответа в зависимости от типа задачи"""
        question = self.context.get('question')
        if not question:
            raise serializers.ValidationError("Контекст задачи не найден")

        question_type = question.question_type

        if question_type == QuestionType.STRING:
            if not isinstance(value, str):
                raise serializers.ValidationError("Ответ должен быть строкой")
        elif question_type == QuestionType.NUMBER:
            try:
                float(value)
            except (ValueError, TypeError):
                raise serializers.ValidationError("Ответ должен быть числом")
        elif question_type in [QuestionType.SEQUENCE_ORDERED, QuestionType.SEQUENCE_UNORDERED]:
            if not isinstance(value, list):
                raise serializers.ValidationError("Ответ должен быть списком")

        return value


class QuestionResultSerializer(serializers.Serializer):
    """Сериализатор для результатов проверки ответов"""
    is_correct = serializers.BooleanField()
    score = serializers.IntegerField()
    feedback = serializers.CharField()
    max_score = serializers.IntegerField()


class QuestionListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка задач"""
    correct_answers_count = serializers.ReadOnlyField()
    options_count = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'question_type', 'max_score',
            'is_active', 'correct_answers_count', 'options_count'
        ]
