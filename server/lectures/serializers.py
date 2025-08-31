from rest_framework import serializers
from .models import Lecture
from graph.serializers import NodeSerializer, ConceptSerializer


class LectureSerializer(serializers.ModelSerializer):
    """Основной сериализатор для лекций"""
    node = NodeSerializer(read_only=True)
    concept = ConceptSerializer(read_only=True)
    entity_type = serializers.CharField(source='get_entity_type', read_only=True)
    vk_embed_code = serializers.CharField(source='get_vk_embed_code', read_only=True)
    
    class Meta:
        model = Lecture
        fields = [
            'id', 'title', 'content', 'node', 'concept', 'entity_type',
            'vk_video_url', 'vk_video_title', 'vk_embed_code',
            'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LectureCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления лекций"""
    
    class Meta:
        model = Lecture
        fields = [
            'title', 'content', 'node', 'concept',
            'vk_video_url', 'vk_video_title',
            'order', 'is_active'
        ]
    
    def validate(self, data):
        """Валидация данных"""
        node = data.get('node')
        concept = data.get('concept')
        
        # Проверяем, что указана ровно одна сущность
        if bool(node) == bool(concept):
            raise serializers.ValidationError(
                'Лекция должна быть привязана либо к узлу, либо к концепту, но не к обоим'
            )
        
        return data
    
    def to_representation(self, instance):
        """Возвращаем полное представление после создания/обновления"""
        return LectureSerializer(instance).data


class LectureListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка лекций"""
    entity_title = serializers.CharField(source='get_entity.title', read_only=True)
    entity_type = serializers.CharField(source='get_entity_type', read_only=True)
    
    class Meta:
        model = Lecture
        fields = [
            'id', 'title', 'entity_title', 'entity_type',
            'order', 'is_active', 'created_at'
        ]
