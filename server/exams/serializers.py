from rest_framework import serializers
from .models import ExamType, ExamSubject, ExamNumber, ExamTopic


class ExamTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типов экзаменов"""
    subjects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamType
        fields = ['id', 'name', 'description', 'is_active', 'order', 'subjects_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_subjects_count(self, obj):
        """Количество активных предметов"""
        return obj.examsubjects.filter(is_active=True).count()


class ExamSubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов экзамена"""
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    subject_name = serializers.CharField(source='subject.title', read_only=True)
    numbers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamSubject
        fields = ['id', 'exam_type', 'exam_type_name', 'subject', 'subject_name', 'is_active', 'order', 'numbers_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_numbers_count(self, obj):
        """Количество активных номеров заданий"""
        return obj.examnumbers.filter(is_active=True).count()


class ExamNumberSerializer(serializers.ModelSerializer):
    """Сериализатор для номеров заданий"""
    exam_subject_info = serializers.SerializerMethodField()
    topics_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamNumber
        fields = ['id', 'exam_subject', 'exam_subject_info', 'number', 'title', 'description', 'is_active', 'order', 'topics_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_exam_subject_info(self, obj):
        """Информация о предмете экзамена"""
        return {
            'exam_type': obj.exam_subject.exam_type.name,
            'subject': obj.exam_subject.subject.title
        }
    
    def get_topics_count(self, obj):
        """Количество активных подтем"""
        return obj.examtopics.filter(is_active=True).count()


class ExamTopicSerializer(serializers.ModelSerializer):
    """Сериализатор для подтем экзамена"""
    exam_number_info = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamTopic
        fields = ['id', 'exam_number', 'exam_number_info', 'title', 'description', 'is_active', 'order', 'questions_count', 'full_path', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_exam_number_info(self, obj):
        """Информация о номере задания"""
        return {
            'number': obj.exam_number.number,
            'title': obj.exam_number.title,
            'exam_type': obj.exam_number.exam_subject.exam_type.name,
            'subject': obj.exam_number.exam_subject.subject.title
        }
    
    def get_questions_count(self, obj):
        """Количество задач"""
        return obj.get_questions_count()
    
    def get_full_path(self, obj):
        """Полный путь к подтеме"""
        return obj.get_full_path()


class ExamTypeDetailSerializer(ExamTypeSerializer):
    """Детальный сериализатор для типов экзаменов с предметами"""
    subjects = ExamSubjectSerializer(many=True, read_only=True, source='examsubjects')
    
    class Meta(ExamTypeSerializer.Meta):
        fields = ExamTypeSerializer.Meta.fields + ['subjects']


class ExamSubjectDetailSerializer(ExamSubjectSerializer):
    """Детальный сериализатор для предметов экзамена с номерами заданий"""
    numbers = ExamNumberSerializer(many=True, read_only=True, source='examnumbers')
    
    class Meta(ExamSubjectSerializer.Meta):
        fields = ExamSubjectSerializer.Meta.fields + ['numbers']


class ExamNumberDetailSerializer(ExamNumberSerializer):
    """Детальный сериализатор для номеров заданий с подтемами"""
    topics = ExamTopicSerializer(many=True, read_only=True, source='examtopics')
    
    class Meta(ExamNumberSerializer.Meta):
        fields = ExamNumberSerializer.Meta.fields + ['topics']


class NavigationSerializer(serializers.Serializer):
    """Сериализатор для навигационной структуры"""
    exam_types = ExamTypeDetailSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        """Получить полную навигационную структуру"""
        exam_types = ExamType.objects.filter(is_active=True).prefetch_related(
            'examsubjects__examnumbers__examtopics'
        )
        return {
            'exam_types': ExamTypeDetailSerializer(exam_types, many=True).data
        }
