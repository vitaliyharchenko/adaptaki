from django.contrib import admin
from django.utils.html import format_html
from .models import ExamType, ExamSubject, ExamNumber, ExamTopic


class ExamSubjectInline(admin.TabularInline):
    """Inline для предметов экзамена"""
    model = ExamSubject
    extra = 1
    ordering = ['order']


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    """Админка для типов экзаменов"""
    list_display = ['name', 'description_short', 'is_active', 'order', 'subjects_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    inlines = [ExamSubjectInline]
    
    def description_short(self, obj):
        """Короткое описание"""
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_short.short_description = 'Описание'
    
    def subjects_count(self, obj):
        """Количество предметов"""
        return obj.examsubjects.filter(is_active=True).count()
    subjects_count.short_description = 'Предметов'


class ExamNumberInline(admin.TabularInline):
    """Inline для номеров заданий"""
    model = ExamNumber
    extra = 1
    ordering = ['order']


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    """Админка для предметов экзамена"""
    list_display = ['exam_type', 'subject', 'is_active', 'order', 'numbers_count', 'created_at']
    list_filter = ['exam_type', 'subject', 'is_active', 'created_at']
    search_fields = ['exam_type__name', 'subject__title']
    ordering = ['exam_type__name', 'order', 'subject__title']
    inlines = [ExamNumberInline]
    
    def numbers_count(self, obj):
        """Количество номеров заданий"""
        return obj.examnumbers.filter(is_active=True).count()
    numbers_count.short_description = 'Заданий'


class ExamTopicInline(admin.TabularInline):
    """Inline для подтем"""
    model = ExamTopic
    extra = 1
    ordering = ['order']


@admin.register(ExamNumber)
class ExamNumberAdmin(admin.ModelAdmin):
    """Админка для номеров заданий"""
    list_display = ['number', 'title', 'exam_subject', 'is_active', 'order', 'topics_count', 'created_at']
    list_filter = ['exam_subject__exam_type', 'exam_subject__subject', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'exam_subject__exam_type__name', 'exam_subject__subject__title']
    ordering = ['exam_subject__exam_type__name', 'exam_subject__subject__title', 'order', 'number']
    inlines = [ExamTopicInline]
    
    def topics_count(self, obj):
        """Количество подтем"""
        return obj.examtopics.filter(is_active=True).count()
    topics_count.short_description = 'Подтем'


@admin.register(ExamTopic)
class ExamTopicAdmin(admin.ModelAdmin):
    """Админка для подтем экзамена"""
    list_display = ['title', 'exam_number_full', 'is_active', 'order', 'questions_count', 'created_at']
    list_filter = ['exam_number__exam_subject__exam_type', 'exam_number__exam_subject__subject', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'exam_number__title']
    ordering = ['exam_number__exam_subject__exam_type__name', 'exam_number__exam_subject__subject__title', 'exam_number__order', 'order']
    
    def exam_number_full(self, obj):
        """Полная информация о номере задания"""
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.exam_number,
            obj.exam_number.exam_subject
        )
    exam_number_full.short_description = 'Номер задания'
    
    def questions_count(self, obj):
        """Количество задач"""
        return obj.get_questions_count()
    questions_count.short_description = 'Задач'
