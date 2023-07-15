from rest_framework import serializers
from apps.graph.serializers import NodeSerializer
from .models import Question, POLICY_CHOICES, TYPE_CHOICES


class PolicyField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in POLICY_CHOICES:
            if t[0] == instance:
                return t[1]
        return instance


class TypeField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in TYPE_CHOICES:
            if t[0] == instance:
                return t[1]
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    checking_policy = PolicyField()
    type = TypeField()

    class Meta:
        model = Question
        fields = ['pk', 'question_text', 'image', 'explanation_image',
                  'max_score', 'type', 'checking_policy', 'nodes', 'trainer_tags']
