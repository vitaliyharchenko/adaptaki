from rest_framework import serializers
from .models import Node, Subject, Concept, TYPE_CHOICES, NodeRelation


class TypeField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in TYPE_CHOICES:
            if t[0] == instance:
                return t[1]
        return instance


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['pk', 'title']


class ConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = ['pk', 'title', 'is_active']


class NodeSerializer(serializers.ModelSerializer):
    type = TypeField()
    subject = SubjectSerializer()
    concept = ConceptSerializer()

    class Meta:
        model = Node
        fields = ['pk', 'title', 'type', 'subject',
                  'concept', 'testability', 'questions_exist']


class NodeRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NodeRelation
        fields = ['pk', 'parent', 'child']
