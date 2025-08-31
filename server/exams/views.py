from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ExamType, ExamSubject, ExamNumber, ExamTopic
from .serializers import (
    ExamTypeSerializer, ExamTypeDetailSerializer,
    ExamSubjectSerializer, ExamSubjectDetailSerializer,
    ExamNumberSerializer, ExamNumberDetailSerializer,
    ExamTopicSerializer, NavigationSerializer
)


class ExamTypeViewSet(viewsets.ModelViewSet):
    """ViewSet для типов экзаменов"""
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve' or self.action == 'subjects':
            return ExamTypeDetailSerializer
        return ExamTypeSerializer

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """Получить предметы для конкретного экзамена"""
        exam_type = self.get_object()
        subjects = exam_type.get_subjects()
        serializer = ExamSubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class ExamSubjectViewSet(viewsets.ModelViewSet):
    """ViewSet для предметов экзамена"""
    queryset = ExamSubject.objects.all()
    serializer_class = ExamSubjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam_type', 'subject', 'is_active']
    search_fields = ['exam_type__name', 'subject__title']
    ordering_fields = ['order', 'created_at']
    ordering = ['exam_type__name', 'order', 'subject__title']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve' or self.action == 'numbers':
            return ExamSubjectDetailSerializer
        return ExamSubjectSerializer

    @action(detail=True, methods=['get'])
    def numbers(self, request, pk=None):
        """Получить номера заданий для конкретного предмета"""
        exam_subject = self.get_object()
        numbers = exam_subject.get_numbers()
        serializer = ExamNumberSerializer(numbers, many=True)
        return Response(serializer.data)


class ExamNumberViewSet(viewsets.ModelViewSet):
    """ViewSet для номеров заданий"""
    queryset = ExamNumber.objects.all()
    serializer_class = ExamNumberSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam_subject', 'is_active']
    search_fields = ['title', 'description', 'exam_subject__exam_type__name', 'exam_subject__subject__title']
    ordering_fields = ['number', 'order', 'created_at']
    ordering = ['exam_subject__exam_type__name', 'exam_subject__subject__title', 'order', 'number']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve' or self.action == 'topics':
            return ExamNumberDetailSerializer
        return ExamNumberSerializer

    @action(detail=True, methods=['get'])
    def topics(self, request, pk=None):
        """Получить подтемы для конкретного номера задания"""
        exam_number = self.get_object()
        topics = exam_number.get_topics()
        serializer = ExamTopicSerializer(topics, many=True)
        return Response(serializer.data)


class ExamTopicViewSet(viewsets.ModelViewSet):
    """ViewSet для подтем экзамена"""
    queryset = ExamTopic.objects.all()
    serializer_class = ExamTopicSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam_number', 'is_active']
    search_fields = ['title', 'description', 'exam_number__title']
    ordering_fields = ['title', 'order', 'created_at']
    ordering = ['exam_number__exam_subject__exam_type__name', 'exam_number__exam_subject__subject__title', 'exam_number__order', 'order']

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Получить задачи для конкретной подтемы"""
        exam_topic = self.get_object()
        questions = exam_topic.get_questions()
        
        # Здесь можно добавить сериализацию задач из приложения questions
        # Пока возвращаем базовую информацию
        questions_data = []
        for question in questions:
            questions_data.append({
                'id': question.id,
                'title': question.title,
                'condition': question.condition[:200] + '...' if len(question.condition) > 200 else question.condition,
                'question_type': question.question_type,
                'max_score': question.max_score,
                'created_at': question.created_at
            })
        
        return Response({
            'topic': ExamTopicSerializer(exam_topic).data,
            'questions': questions_data,
            'questions_count': len(questions_data)
        })


class NavigationViewSet(viewsets.ViewSet):
    """ViewSet для навигационной структуры"""
    
    def list(self, request):
        """Получить полную навигационную структуру"""
        serializer = NavigationSerializer(data={})
        serializer.is_valid()
        return Response(serializer.data)
