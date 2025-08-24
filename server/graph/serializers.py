from rest_framework import serializers
from .models import Subject, Concept, Node, NodeRelation


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class NodeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeRelation
        fields = '__all__'
