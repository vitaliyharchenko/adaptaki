from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Subject, Concept, Node, NodeRelation
from .serializers import (
    SubjectSerializer, 
    ConceptSerializer, 
    NodeSerializer, 
    NodeRelationSerializer
)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ConceptViewSet(viewsets.ModelViewSet):
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'concept']
    search_fields = ['title']


class NodeRelationViewSet(viewsets.ModelViewSet):
    queryset = NodeRelation.objects.all()
    serializer_class = NodeRelationSerializer
