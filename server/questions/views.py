from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
import random

from .models import Question, QuestionOption, QuestionType, GradingPolicy
from .serializers import (
    QuestionSerializer, QuestionCreateSerializer, QuestionListSerializer,
    QuestionAnswerSerializer, QuestionResultSerializer
)





class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet для задач"""
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['question_type', 'is_active',
                        'nodes__subject', 'nodes__concept']
    search_fields = ['title', 'condition']
    ordering_fields = ['created_at', 'title', 'max_score']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return QuestionCreateSerializer
        elif self.action == 'list':
            return QuestionListSerializer
        return QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по узлам графа
        node_id = self.request.query_params.get('node_id')
        if node_id:
            queryset = queryset.filter(nodes__id=node_id)

        # Фильтрация по предмету
        subject_id = self.request.query_params.get('subject_id')
        if subject_id:
            queryset = queryset.filter(nodes__subject__id=subject_id)

        # Фильтрация по концепту
        concept_id = self.request.query_params.get('concept_id')
        if concept_id:
            queryset = queryset.filter(nodes__concept__id=concept_id)

        # Только активные задачи
        if self.request.query_params.get('active_only', 'true').lower() == 'true':
            queryset = queryset.filter(is_active=True)

        return queryset.prefetch_related('options', 'nodes', 'analogs')

    @action(detail=True, methods=['post'])
    def check_answer(self, request, pk=None):
        """Проверить ответ на задачу"""
        question = self.get_object()

        serializer = QuestionAnswerSerializer(
            data=request.data,
            context={'question': question}
        )

        if serializer.is_valid():
            user_answer = serializer.validated_data['answer']
            is_correct, score, feedback = question.check_answer(user_answer)

            result_serializer = QuestionResultSerializer({
                'is_correct': is_correct,
                'score': score,
                'feedback': feedback,
                'max_score': question.max_score
            })

            return Response(result_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_random_analog(self, request, pk=None):
        """Получить случайную аналогичную задачу"""
        question = self.get_object()

        # Получаем все аналогичные задачи
        analogs = question.analogs.filter(is_active=True)

        if not analogs.exists():
            return Response(
                {'error': 'Нет аналогичных задач'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Выбираем случайную
        random_analog = random.choice(analogs)
        serializer = self.get_serializer(random_analog)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def random_by_node(self, request):
        """Получить случайную задачу по узлу графа"""
        node_id = request.query_params.get('node_id')
        if not node_id:
            return Response(
                {'error': 'Необходимо указать node_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        questions = self.get_queryset().filter(nodes__id=node_id)

        if not questions.exists():
            return Response(
                {'error': 'Нет задач для данного узла'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Выбираем случайную задачу
        random_question = random.choice(questions)

        # Если у задачи есть аналоги, выбираем случайную из группы
        if random_question.analogs.exists():
            all_analogs = list(random_question.analogs.filter(
                is_active=True)) + [random_question]
            final_question = random.choice(all_analogs)
        else:
            final_question = random_question

        serializer = self.get_serializer(final_question)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Получить статистику по задачам"""
        queryset = self.get_queryset()

        stats = {
            'total_questions': queryset.count(),
            'active_questions': queryset.filter(is_active=True).count(),
            'by_type': {},
            'by_subject': {},
            'by_concept': {}
        }

        # Статистика по типам
        for question_type in QuestionType.choices:
            count = queryset.filter(question_type=question_type[0]).count()
            stats['by_type'][question_type[1]] = count

        # Статистика по предметам
        subjects = queryset.values('nodes__subject__title').annotate(
            count=Count('id')
        ).filter(nodes__subject__title__isnull=False)

        for subject in subjects:
            stats['by_subject'][subject['nodes__subject__title']] = subject['count']

        # Статистика по концептам
        concepts = queryset.values('nodes__concept__title').annotate(
            count=Count('id')
        ).filter(nodes__concept__title__isnull=False)

        for concept in concepts:
            stats['by_concept'][concept['nodes__concept__title']] = concept['count']

        return Response(stats)

    @action(detail=True, methods=['post'])
    def copy(self, request, pk=None):
        """Скопировать задачу"""
        question = self.get_object()

        # Создаем копию
        new_question = Question.objects.create(
            title=f"{question.title} (копия)",
            condition=question.condition,
            solution=question.solution,
            question_type=question.question_type,
            max_score=question.max_score,
            grading_policy=question.grading_policy,
            precision=question.precision,
            is_active=False  # Копия неактивна по умолчанию
        )

        # Копируем связи
        new_question.nodes.set(question.nodes.all())
        new_question.analogs.set(question.analogs.all())

        # Копируем варианты ответов
        for option in question.options.all():
            QuestionOption.objects.create(
                question=new_question,
                text=option.text,
                is_correct=option.is_correct,
                order=option.order
            )

        serializer = self.get_serializer(new_question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_analog(self, request, pk=None):
        """Добавить аналогичную задачу"""
        question = self.get_object()
        analog_id = request.data.get('analog_id')

        if not analog_id:
            return Response(
                {'error': 'Необходимо указать analog_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            analog_question = Question.objects.get(id=analog_id)
            question.analogs.add(analog_question)
            analog_question.analogs.add(question)  # Обратная связь

            return Response({'message': 'Аналогичная задача добавлена'})
        except Question.DoesNotExist:
            return Response(
                {'error': 'Задача не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['delete'])
    def remove_analog(self, request, pk=None):
        """Удалить аналогичную задачу"""
        question = self.get_object()
        analog_id = request.query_params.get('analog_id')

        if not analog_id:
            return Response(
                {'error': 'Необходимо указать analog_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            analog_question = Question.objects.get(id=analog_id)
            question.analogs.remove(analog_question)
            analog_question.analogs.remove(question)  # Обратная связь

            return Response({'message': 'Аналогичная задача удалена'})
        except Question.DoesNotExist:
            return Response(
                {'error': 'Задача не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )



