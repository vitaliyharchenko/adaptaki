from rest_framework import serializers
from apps.graph.serializers import NodeSerializer
from .models import Question, POLICY_CHOICES, TYPE_CHOICES, QuestionOption


# Расшифровка метода проверки
class PolicyField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in POLICY_CHOICES:
            if t[0] == instance:
                return t[1]
        return instance


# Расшифровка типа задачи
class TypeField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in TYPE_CHOICES:
            if t[0] == instance:
                return t[1]
        return instance


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionOption
        fields = ['pk', 'is_true', 'option_text', 'option_image']


class QuestionAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(required=True, max_length=200)


class QuestionSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    checking_policy = PolicyField()
    type = TypeField()

    class Meta:
        model = Question
        fields = ['pk', 'question_text', 'image', 'explanation_image',
                  'max_score', 'type', 'checking_policy', 'nodes', 'exam_tag']


class QuestionSerializerWithAnswer(QuestionSerializer):
    all_options = OptionSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ['pk', 'question_text', 'image', 'explanation_image',
                  'max_score', 'type', 'checking_policy', 'all_options', 'nodes', 'exam_tag']
