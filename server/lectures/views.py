import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Lecture
from .serializers import (
    LectureSerializer, 
    LectureCreateUpdateSerializer, 
    LectureListSerializer
)


# Create your views here.

@csrf_exempt
def upload_image(request):
    """
    Обработчик загрузки изображений для TinyMCE
    """
    if request.method == 'POST':
        image = request.FILES.get('file')
        if image:
            # Проверяем тип файла
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_types:
                return JsonResponse({
                    'error': 'Неподдерживаемый тип файла. Разрешены только JPEG, PNG, GIF, WebP'
                }, status=400)
            
            # Проверяем размер файла (максимум 5MB)
            if image.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'error': 'Файл слишком большой. Максимальный размер: 5MB'
                }, status=400)
            
            # Генерируем уникальное имя файла
            file_extension = image.name.split('.')[-1]
            filename = f"lectures/images/{uuid.uuid4()}.{file_extension}"
            
            # Сохраняем файл
            try:
                with default_storage.open(filename, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                
                return JsonResponse({
                    'location': default_storage.url(filename)
                })
            except Exception as e:
                return JsonResponse({
                    'error': f'Ошибка при сохранении файла: {str(e)}'
                }, status=500)
        
        return JsonResponse({
            'error': 'Файл не найден'
        }, status=400)
    
    return JsonResponse({
        'error': 'Метод не поддерживается'
    }, status=405)


class LectureViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с лекциями
    """
    queryset = Lecture.objects.select_related('node', 'concept', 'node__subject', 'concept__subject')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'node', 'concept', 'node__subject', 'concept__subject']
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'order', 'created_at']
    ordering = ['order', 'title']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action in ['create', 'update', 'partial_update']:
            return LectureCreateUpdateSerializer
        elif self.action == 'list':
            return LectureListSerializer
        return LectureSerializer
    
    def get_queryset(self):
        """Фильтрация queryset"""
        queryset = super().get_queryset()
        
        # Фильтрация по типу сущности
        entity_type = self.request.query_params.get('entity_type')
        if entity_type:
            if entity_type == 'node':
                queryset = queryset.filter(node__isnull=False)
            elif entity_type == 'concept':
                queryset = queryset.filter(concept__isnull=False)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_node(self, request):
        """Получить лекции для конкретного узла"""
        node_id = request.query_params.get('node_id')
        if not node_id:
            return Response(
                {'error': 'node_id параметр обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lectures = self.get_queryset().filter(node_id=node_id, is_active=True)
        serializer = self.get_serializer(lectures, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_concept(self, request):
        """Получить лекции для конкретного концепта"""
        concept_id = request.query_params.get('concept_id')
        if not concept_id:
            return Response(
                {'error': 'concept_id параметр обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lectures = self.get_queryset().filter(concept_id=concept_id, is_active=True)
        serializer = self.get_serializer(lectures, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def with_entity_info(self, request, pk=None):
        """Получить лекцию с подробной информацией о связанной сущности"""
        lecture = self.get_object()
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)
